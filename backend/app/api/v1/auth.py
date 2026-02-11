"""Authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from pydantic import EmailStr

from app.db.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.email_token import EmailToken
from app.schemas.auth import (
    UserSignup, UserLogin, Token, UserResponse,
    EmailVerificationRequest, PasswordResetRequest,
    PasswordResetConfirm, PasswordChange
)
from app.core.security import (
    verify_password, get_password_hash, create_access_token,
    generate_verification_token, generate_password_reset_token,
    generate_verification_code, decode_access_token
)
from app.core.email import send_verification_email, send_password_reset_email
from app.core.config import settings

router = APIRouter()

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Dependency to get current user from JWT token
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username.lower()).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username.lower(),
        password_hash=get_password_hash(user_data.password),
        name=user_data.name,
        email_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create user profile
    user_profile = UserProfile(user_id=new_user.id)
    db.add(user_profile)
    db.commit()
    
    # Generate verification token and code
    verification_token = generate_verification_token()
    verification_code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(minutes=15)  # 15 minutes expiry
    
    email_token = EmailToken(
        user_id=new_user.id,
        token=verification_token,
        code=verification_code,
        token_type="verification",
        expires_at=expires_at
    )
    
    db.add(email_token)
    db.commit()
    
    # Send verification email (async, don't wait)
    try:
        await send_verification_email(user_data.email, user_data.name, verification_code)
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        # Don't fail signup if email fails
    
    return {
        "message": "User created successfully. Please check your email for the verification code.",
        "user_id": new_user.id,
        "email": new_user.email
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    
    # Find user by email or username
    user = db.query(User).filter(
        (User.email == credentials.email_or_username) |
        (User.username == credentials.email_or_username.lower())
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }

@router.post("/verify-email")
async def verify_email(request: EmailVerificationRequest, db: Session = Depends(get_db)):
    """Verify user email with code"""
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Find token by code and user
    email_token = db.query(EmailToken).filter(
        EmailToken.user_id == user.id,
        EmailToken.code == request.code,
        EmailToken.token_type == "verification",
        EmailToken.used == False
    ).first()
    
    if not email_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    # Check if token expired
    if email_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired. Please request a new one."
        )
    
    # Mark email as verified
    user.email_verified = True
    email_token.used = True
    
    db.commit()
    
    return {"message": "Email verified successfully"}

@router.post("/resend-verification")
async def resend_verification(email: EmailStr, db: Session = Depends(get_db)):
    """Resend verification code"""
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Don't reveal if email exists
        return {"message": "If the email exists, a verification code has been sent"}
    
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Invalidate old tokens
    db.query(EmailToken).filter(
        EmailToken.user_id == user.id,
        EmailToken.token_type == "verification"
    ).update({"used": True})
    
    # Generate new token and code
    verification_token = generate_verification_token()
    verification_code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    
    email_token = EmailToken(
        user_id=user.id,
        token=verification_token,
        code=verification_code,
        token_type="verification",
        expires_at=expires_at
    )
    
    db.add(email_token)
    db.commit()
    
    # Send email
    try:
        await send_verification_email(user.email, user.name, verification_code)
    except Exception as e:
        print(f"Failed to send verification email: {e}")
    
    return {"message": "If the email exists, a verification code has been sent"}

@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Request password reset code"""
    
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Don't reveal if email exists
        return {"message": "If the email exists, a password reset code has been sent"}
    
    # Invalidate old tokens
    db.query(EmailToken).filter(
        EmailToken.user_id == user.id,
        EmailToken.token_type == "password_reset"
    ).update({"used": True})
    
    # Generate reset token and code
    reset_token = generate_password_reset_token()
    reset_code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(minutes=15)  # 15 minutes expiry
    
    email_token = EmailToken(
        user_id=user.id,
        token=reset_token,
        code=reset_code,
        token_type="password_reset",
        expires_at=expires_at
    )
    
    db.add(email_token)
    db.commit()
    
    # Send email
    try:
        await send_password_reset_email(user.email, user.name, reset_code)
    except Exception as e:
        print(f"Failed to send password reset email: {e}")
    
    return {"message": "If the email exists, a password reset code has been sent"}

@router.post("/reset-password")
async def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Reset password with code"""
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Find token by code and user
    email_token = db.query(EmailToken).filter(
        EmailToken.user_id == user.id,
        EmailToken.code == request.code,
        EmailToken.token_type == "password_reset",
        EmailToken.used == False
    ).first()
    
    if not email_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset code"
        )
    
    # Check if token expired
    if email_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset code has expired. Please request a new one."
        )
    
    # Update password
    user.password_hash = get_password_hash(request.new_password)
    email_token.used = True
    
    db.commit()
    
    return {"message": "Password reset successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return UserResponse.from_orm(current_user)

@router.post("/change-password")
async def change_password(
    request: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password for logged-in user"""
    
    # Verify current password
    if not verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password_hash = get_password_hash(request.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}
