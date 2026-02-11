"""Security utilities for authentication"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
import secrets
import random

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    # Truncate password to bcrypt's 72-byte limit before verification
    safe_password = password_to_bcrypt_safe(plain_password)
    return pwd_context.verify(safe_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password with bcrypt
    
    Note: bcrypt has a hard limit of 72 bytes. Passwords longer than this
    will be truncated to prevent crashes.
    """
    # Truncate password to bcrypt's 72-byte limit
    safe_password = password_to_bcrypt_safe(password)
    return pwd_context.hash(safe_password)

def password_to_bcrypt_safe(password: str) -> str:
    """
    Truncate password to bcrypt's 72-byte limit
    
    bcrypt has a hard technical limit of 72 bytes. This function ensures
    passwords don't exceed this limit to prevent ValueError crashes.
    """
    # Encode to bytes, truncate to 72 bytes, decode back to string
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        # Truncate to 72 bytes and decode, ignoring any incomplete characters
        safe_password = password_bytes[:72].decode("utf-8", errors="ignore")
        return safe_password
    return password

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_verification_token() -> str:
    """Generate a secure random token for email verification"""
    return secrets.token_urlsafe(32)

def generate_password_reset_token() -> str:
    """Generate a secure random token for password reset"""
    return secrets.token_urlsafe(32)

def generate_verification_code() -> str:
    """Generate a 6-digit verification code"""
    return str(random.randint(100000, 999999))
