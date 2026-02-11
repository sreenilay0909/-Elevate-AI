"""AI Analysis API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User
from app.models.platform_data import PlatformData
from app.api.v1.auth import get_current_user
from app.services.ai_analysis_service import AIAnalysisService

router = APIRouter()

# Request/Response Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    chatHistory: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    answer: str
    platform: str

class AnalysisResponse(BaseModel):
    platform: str
    username: str
    percentileRank: float
    globalRanking: str
    overallScore: float
    strengths: List[dict]
    weaknesses: List[dict]
    recommendations: List[str]
    weeklyPlan: dict
    keyMetrics: List[dict]
    topicBreakdown: Optional[List[dict]] = None
    analyzedAt: str

@router.get("/analyze/{platform}", response_model=AnalysisResponse)
async def analyze_platform(
    platform: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI analysis for a specific platform
    
    This endpoint:
    1. Retrieves stored platform data
    2. Performs comprehensive AI analysis
    3. Returns percentile ranking, strengths, weaknesses, and improvement plan
    """
    
    # Get platform data
    platform_data = db.query(PlatformData).filter(
        PlatformData.user_id == current_user.id,
        PlatformData.platform_name == platform
    ).first()
    
    if not platform_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for platform: {platform}. Please fetch data first."
        )
    
    if not platform_data.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Platform data is empty for {platform}"
        )
    
    # Get username from data
    username = platform_data.data.get('username', 'unknown')
    
    # Perform AI analysis
    try:
        ai_service = AIAnalysisService()
        analysis = ai_service.analyze_platform_data(
            platform=platform,
            user_data=platform_data.data,
            username=username
        )
        
        return AnalysisResponse(**analysis)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"AI Analysis Error: {error_details}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI analysis failed: {str(e)}"
        )

@router.post("/chat/{platform}", response_model=ChatResponse)
async def chat_with_platform(
    platform: str,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Platform-specific Q&A chatbot
    
    This chatbot:
    1. Only answers questions about the specific platform
    2. Uses user's actual data for context
    3. Provides personalized advice
    """
    
    # Get platform data
    platform_data = db.query(PlatformData).filter(
        PlatformData.user_id == current_user.id,
        PlatformData.platform_name == platform
    ).first()
    
    if not platform_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for platform: {platform}"
        )
    
    # Get username
    username = platform_data.data.get('username', 'unknown')
    
    # Get or create analysis
    try:
        ai_service = AIAnalysisService()
        
        # First get analysis for context
        analysis = ai_service.analyze_platform_data(
            platform=platform,
            user_data=platform_data.data,
            username=username
        )
        
        # Convert chat history to proper format
        chat_history = []
        if chat_request.chatHistory:
            chat_history = [
                {"role": msg.role, "content": msg.content}
                for msg in chat_request.chatHistory
            ]
        
        # Get chat response
        answer = ai_service.chat_with_platform_context(
            platform=platform,
            user_data=platform_data.data,
            analysis=analysis,
            question=chat_request.question,
            chat_history=chat_history
        )
        
        return ChatResponse(
            answer=answer,
            platform=platform
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )
