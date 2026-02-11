from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.profile import ProfileRequest, AnalysisResponse
from app.services.github_service import GitHubService
from app.services.leetcode_service import LeetCodeService
from app.services.resume_service import ResumeService
from app.services.ai_service import AIService
from app.core.config import settings
from typing import List, Dict, Any, Optional

router = APIRouter()

# Initialize services
github_service = GitHubService(settings.GITHUB_TOKEN)
leetcode_service = LeetCodeService()
resume_service = ResumeService(settings.GEMINI_API_KEY)
ai_service = AIService(settings.GEMINI_API_KEY)

@router.post("/complete")
async def analyze_complete_profile(request: ProfileRequest):
    """
    Analyze complete profile across all platforms and generate comprehensive report
    """
    try:
        platform_scores = []
        errors = []
        
        # GitHub analysis
        if request.github_username:
            try:
                github_result = github_service.analyze_profile(request.github_username)
                platform_scores.append(github_result)
            except Exception as e:
                errors.append(f"GitHub: {str(e)}")
        
        # LeetCode analysis
        if request.leetcode_username:
            try:
                leetcode_result = leetcode_service.analyze_profile(request.leetcode_username)
                platform_scores.append(leetcode_result)
            except Exception as e:
                errors.append(f"LeetCode: {str(e)}")
        
        # Check if we have at least one platform analyzed
        if not platform_scores:
            error_msg = "No platforms could be analyzed. "
            if errors:
                error_msg += "Errors: " + "; ".join(errors)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Calculate composite score
        composite_score = sum(p["score"] for p in platform_scores) / len(platform_scores)
        
        # Generate AI recommendations
        try:
            ai_analysis = ai_service.generate_recommendations(
                platform_scores,
                request.target_role or "Software Engineer"
            )
        except Exception as e:
            # Use fallback if AI fails
            ai_analysis = ai_service._generate_fallback_recommendations(
                platform_scores,
                request.target_role or "Software Engineer"
            )
        
        # Construct response - return as dict for proper serialization
        return {
            "compositeScore": round(composite_score, 2),
            "platformScores": platform_scores,
            "marketAnalysis": ai_analysis.get("market_analysis", {}),
            "recommendations": ai_analysis.get("recommendations", []),
            "roadmap": ai_analysis.get("roadmap", []),
            "jobMatch": ai_analysis.get("job_match", {
                "role": request.target_role or "Software Engineer",
                "fitPercent": round(composite_score, 2),
                "gaps": []
            }),
            "jobListings": []
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/complete-with-resume")
async def analyze_with_resume(
    github_username: Optional[str] = Form(None),
    leetcode_username: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None),
    target_role: Optional[str] = Form("Software Engineer"),
    resume_file: UploadFile = File(...)
):
    """
    Analyze complete profile including resume file upload
    """
    try:
        platform_scores = []
        errors = []
        
        # GitHub analysis
        if github_username:
            try:
                github_result = github_service.analyze_profile(github_username)
                platform_scores.append(github_result)
            except Exception as e:
                errors.append(f"GitHub: {str(e)}")
        
        # LeetCode analysis
        if leetcode_username:
            try:
                leetcode_result = leetcode_service.analyze_profile(leetcode_username)
                platform_scores.append(leetcode_result)
            except Exception as e:
                errors.append(f"LeetCode: {str(e)}")
        
        # Resume analysis
        if resume_file:
            try:
                # Read file content
                file_content = await resume_file.read()
                
                # Validate file size (max 10MB)
                if len(file_content) > 10 * 1024 * 1024:
                    raise ValueError("File size exceeds 10MB limit")
                
                # Analyze resume
                resume_result = await resume_service.analyze_resume_file(
                    file_content,
                    resume_file.filename
                )
                platform_scores.append(resume_result)
            except Exception as e:
                errors.append(f"Resume: {str(e)}")
        
        # Check if we have at least one platform analyzed
        if not platform_scores:
            error_msg = "No platforms could be analyzed. "
            if errors:
                error_msg += "Errors: " + "; ".join(errors)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Calculate composite score
        composite_score = sum(p["score"] for p in platform_scores) / len(platform_scores)
        
        # Generate AI recommendations
        try:
            ai_analysis = ai_service.generate_recommendations(
                platform_scores,
                target_role or "Software Engineer"
            )
        except Exception as e:
            ai_analysis = ai_service._generate_fallback_recommendations(
                platform_scores,
                target_role or "Software Engineer"
            )
        
        # Construct response - return as dict with camelCase
        return {
            "compositeScore": round(composite_score, 2),
            "platformScores": platform_scores,
            "marketAnalysis": ai_analysis.get("market_analysis", {}),
            "recommendations": ai_analysis.get("recommendations", []),
            "roadmap": ai_analysis.get("roadmap", []),
            "jobMatch": ai_analysis.get("job_match", {
                "role": target_role or "Software Engineer",
                "fitPercent": round(composite_score, 2),
                "gaps": []
            }),
            "jobListings": []
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/github/{username}")
async def analyze_github(username: str):
    """Analyze GitHub profile only"""
    try:
        result = github_service.analyze_profile(username)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/leetcode/{username}")
async def analyze_leetcode(username: str):
    """Analyze LeetCode profile only"""
    try:
        result = leetcode_service.analyze_profile(username)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/resume-only")
async def analyze_resume_only(resume_file: UploadFile = File(...)):
    """Analyze resume file only"""
    try:
        # Read file content
        file_content = await resume_file.read()
        
        # Validate file size (max 10MB)
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        
        # Analyze resume
        result = await resume_service.analyze_resume_file(
            file_content,
            resume_file.filename
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "github": "configured" if settings.GITHUB_TOKEN else "not configured",
            "gemini": "configured" if settings.GEMINI_API_KEY else "not configured"
        }
    }
