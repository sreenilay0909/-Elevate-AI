"""User profile management endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.api.v1.auth import get_current_user
from app.schemas.profile import (
    ProfileUpdate, ProfileResponse, PublicProfileResponse
)

router = APIRouter()

def build_profile_response(profile: UserProfile, user: User) -> ProfileResponse:
    """Helper to build ProfileResponse"""
    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        username=user.username,
        name=user.name,
        email=user.email,
        github_username=profile.github_username,
        leetcode_username=profile.leetcode_username,
        geeksforgeeks_username=profile.geeksforgeeks_username,
        codechef_username=profile.codechef_username,
        hackerrank_username=profile.hackerrank_username,
        devpost_username=profile.devpost_username,
        devto_username=profile.devto_username,
        linkedin_url=profile.linkedin_url,
        resume_url=profile.resume_url,
        portfolio_url=profile.portfolio_url,
        full_name=profile.full_name,
        gender=profile.gender,
        profile_picture_url=profile.profile_picture_url,
        contact_number=profile.contact_number,
        bio=profile.bio,
        college_name=profile.college_name,
        degree=profile.degree,
        field_of_study=profile.field_of_study,
        current_year=profile.current_year,
        graduation_year=profile.graduation_year,
        skills=profile.skills,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        # Create profile if doesn't exist
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return build_profile_response(profile, current_user)

@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    
    # Update fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    return build_profile_response(profile, current_user)

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload resume file (PDF only)"""
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    # Validate file size (max 5MB)
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 5MB"
        )
    
    # Create uploads directory if it doesn't exist
    import os
    uploads_dir = "uploads/resumes"
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Generate unique filename
    import uuid
    from datetime import datetime
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{current_user.username}_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d')}.{file_extension}"
    file_path = os.path.join(uploads_dir, unique_filename)
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Update profile with resume URL
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    
    # Delete old resume file if exists
    if profile.resume_url:
        old_file_path = profile.resume_url.replace('/uploads/', 'uploads/')
        if os.path.exists(old_file_path):
            try:
                os.remove(old_file_path)
            except:
                pass
    
    profile.resume_url = f"/uploads/resumes/{unique_filename}"
    db.commit()
    db.refresh(profile)
    
    return {
        "message": "Resume uploaded successfully",
        "resume_url": profile.resume_url,
        "filename": file.filename
    }

@router.post("/upload-profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload profile picture (images only)"""
    
    # Validate file type
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    file_ext = '.' + file.filename.split('.')[-1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files (JPG, PNG, GIF, WEBP) are allowed"
        )
    
    # Validate file size (max 2MB)
    content = await file.read()
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 2MB"
        )
    
    # Create uploads directory if it doesn't exist
    import os
    uploads_dir = "uploads/profile_pictures"
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Generate unique filename
    import uuid
    from datetime import datetime
    unique_filename = f"{current_user.username}_profile_{uuid.uuid4().hex[:8]}{file_ext}"
    file_path = os.path.join(uploads_dir, unique_filename)
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Update profile with profile picture URL
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    
    # Delete old profile picture if exists
    if profile.profile_picture_url:
        old_file_path = profile.profile_picture_url.replace('/uploads/', 'uploads/')
        if os.path.exists(old_file_path):
            try:
                os.remove(old_file_path)
            except:
                pass
    
    profile.profile_picture_url = f"/uploads/profile_pictures/{unique_filename}"
    db.commit()
    db.refresh(profile)
    
    return {
        "message": "Profile picture uploaded successfully",
        "profile_picture_url": profile.profile_picture_url,
        "filename": file.filename
    }

@router.delete("/delete-resume")
async def delete_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete resume file"""
    
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile or not profile.resume_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume found"
        )
    
    # Delete file
    import os
    file_path = profile.resume_url.replace('/uploads/', 'uploads/')
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file: {str(e)}"
            )
    
    # Update profile
    profile.resume_url = None
    db.commit()
    
    return {"message": "Resume deleted successfully"}

@router.get("/{username}", response_model=PublicProfileResponse)
async def get_public_profile(
    username: str,
    db: Session = Depends(get_db)
):
    """Get public profile by username"""
    
    user = db.query(User).filter(User.username == username.lower()).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user.id
    ).first()
    
    if not profile:
        profile = UserProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return PublicProfileResponse(
        username=user.username,
        name=user.name,
        email=user.email,
        github_username=profile.github_username,
        leetcode_username=profile.leetcode_username,
        geeksforgeeks_username=profile.geeksforgeeks_username,
        codechef_username=profile.codechef_username,
        hackerrank_username=profile.hackerrank_username,
        devpost_username=profile.devpost_username,
        devto_username=profile.devto_username,
        linkedin_url=profile.linkedin_url,
        portfolio_url=profile.portfolio_url,
        resume_url=profile.resume_url,
        full_name=profile.full_name,
        gender=profile.gender,
        profile_picture_url=profile.profile_picture_url,
        contact_number=profile.contact_number,
        bio=profile.bio,
        college_name=profile.college_name,
        degree=profile.degree,
        field_of_study=profile.field_of_study,
        current_year=profile.current_year,
        graduation_year=profile.graduation_year,
        skills=profile.skills,
        created_at=profile.created_at
    )

@router.get("/search/users")
async def search_users(
    q: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Search users by username or name"""
    
    if not q or len(q) < 2:
        return []
    
    search_term = f"%{q.lower()}%"
    
    users = db.query(User).filter(
        (User.username.like(search_term)) | (User.name.like(search_term))
    ).limit(limit).all()
    
    results = []
    for user in users:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == user.id
        ).first()
        
        results.append({
            "username": user.username,
            "name": user.name,
            "fullName": profile.full_name if profile else None,
            "bio": profile.bio[:100] + "..." if profile and profile.bio and len(profile.bio) > 100 else profile.bio if profile else None,
            "collegeName": profile.college_name if profile else None,
        })
    
    return results

