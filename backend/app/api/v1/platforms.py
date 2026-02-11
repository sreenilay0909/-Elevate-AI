"""Platform data API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.platform_data import PlatformData
from app.api.v1.auth import get_current_user
from app.schemas.platform_schemas import (
    PlatformDataResponse, FetchResponse, FetchAllResponse,
    convert_dict_keys_to_camel
)
from app.services.platform_service_updated import (
    GitHubServiceUpdated, LeetCodeServiceUpdated, GeeksforGeeksService,
    CodeChefService, HackerRankService, DevPostService, DevToService,
    LinkedInService
)
from app.core.config import settings

router = APIRouter()

# Platform service mapping
PLATFORM_SERVICES = {
    "github": lambda: GitHubServiceUpdated(settings.GITHUB_TOKEN),
    "leetcode": lambda: LeetCodeServiceUpdated(),
    "geeksforgeeks": lambda: GeeksforGeeksService(),
    "codechef": lambda: CodeChefService(),
    "hackerrank": lambda: HackerRankService(),
    "devpost": lambda: DevPostService(),
    "devto": lambda: DevToService(),
    "linkedin": lambda: LinkedInService(),
}

@router.post("/fetch/{platform}", response_model=FetchResponse)
async def fetch_platform_data(
    platform: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch data for a single platform"""
    
    # Validate platform
    if platform not in PLATFORM_SERVICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid platform: {platform}"
        )
    
    # Get user profile
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    # Get username for platform
    if platform == "linkedin":
        # LinkedIn uses URL instead of username
        username_field = "linkedin_url"
    else:
        username_field = f"{platform}_username"
    
    username = getattr(profile, username_field, None)
    
    if not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No username configured for {platform}"
        )
    
    # Fetch data from platform
    try:
        service = PLATFORM_SERVICES[platform]()
        data = service.fetch_user_data(username)
        
        # Store in database
        platform_data = db.query(PlatformData).filter(
            PlatformData.user_id == current_user.id,
            PlatformData.platform_name == platform
        ).first()
        
        if platform_data:
            platform_data.data = data
            platform_data.last_updated = datetime.utcnow()
            platform_data.update_status = "success"
            platform_data.error_message = None
        else:
            platform_data = PlatformData(
                user_id=current_user.id,
                platform_name=platform,
                data=data,
                update_status="success"
            )
            db.add(platform_data)
        
        db.commit()
        db.refresh(platform_data)
        
        return FetchResponse(
            platform=platform,
            status="success",
            data=convert_dict_keys_to_camel(data),
            last_updated=platform_data.last_updated
        )
    
    except ValueError as e:
        # Store error in database
        platform_data = db.query(PlatformData).filter(
            PlatformData.user_id == current_user.id,
            PlatformData.platform_name == platform
        ).first()
        
        if platform_data:
            platform_data.update_status = "error"
            platform_data.error_message = str(e)
            platform_data.last_updated = datetime.utcnow()
            db.commit()
        
        return FetchResponse(
            platform=platform,
            status="error",
            error=str(e)
        )
    except Exception as e:
        return FetchResponse(
            platform=platform,
            status="error",
            error=f"Unexpected error: {str(e)}"
        )

@router.post("/fetch-all", response_model=FetchAllResponse)
async def fetch_all_platforms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch data for all configured platforms"""
    
    # Get user profile
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    results = []
    successful = 0
    failed = 0
    
    # Fetch data for each platform
    for platform in PLATFORM_SERVICES.keys():
        if platform == "linkedin":
            username_field = "linkedin_url"
        else:
            username_field = f"{platform}_username"
        
        username = getattr(profile, username_field, None)
        
        if not username:
            continue  # Skip platforms without username
        
        try:
            service = PLATFORM_SERVICES[platform]()
            data = service.fetch_user_data(username)
            
            # Store in database
            platform_data = db.query(PlatformData).filter(
                PlatformData.user_id == current_user.id,
                PlatformData.platform_name == platform
            ).first()
            
            if platform_data:
                platform_data.data = data
                platform_data.last_updated = datetime.utcnow()
                platform_data.update_status = "success"
                platform_data.error_message = None
            else:
                platform_data = PlatformData(
                    user_id=current_user.id,
                    platform_name=platform,
                    data=data,
                    update_status="success"
                )
                db.add(platform_data)
            
            db.commit()
            db.refresh(platform_data)
            
            results.append(FetchResponse(
                platform=platform,
                status="success",
                data=convert_dict_keys_to_camel(data),
                last_updated=platform_data.last_updated
            ))
            successful += 1
        
        except Exception as e:
            # Store error
            platform_data = db.query(PlatformData).filter(
                PlatformData.user_id == current_user.id,
                PlatformData.platform_name == platform
            ).first()
            
            if platform_data:
                platform_data.update_status = "error"
                platform_data.error_message = str(e)
                platform_data.last_updated = datetime.utcnow()
                db.commit()
            
            results.append(FetchResponse(
                platform=platform,
                status="error",
                error=str(e)
            ))
            failed += 1
    
    return FetchAllResponse(
        results=results,
        total=len(results),
        successful=successful,
        failed=failed
    )

@router.get("/data/{platform}", response_model=PlatformDataResponse)
async def get_platform_data(
    platform: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get stored data for a single platform"""
    
    platform_data = db.query(PlatformData).filter(
        PlatformData.user_id == current_user.id,
        PlatformData.platform_name == platform
    ).first()
    
    if not platform_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for platform: {platform}"
        )
    
    return PlatformDataResponse(
        platform=platform_data.platform_name,
        data=convert_dict_keys_to_camel(platform_data.data),
        last_updated=platform_data.last_updated,
        fetch_status=platform_data.update_status,
        error_message=platform_data.error_message
    )

@router.get("/data", response_model=List[PlatformDataResponse])
async def get_all_platform_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get stored data for all platforms"""
    
    platform_data_list = db.query(PlatformData).filter(
        PlatformData.user_id == current_user.id
    ).all()
    
    return [
        PlatformDataResponse(
            platform=pd.platform_name,
            data=convert_dict_keys_to_camel(pd.data),
            last_updated=pd.last_updated,
            fetch_status=pd.update_status,
            error_message=pd.error_message
        )
        for pd in platform_data_list
    ]
