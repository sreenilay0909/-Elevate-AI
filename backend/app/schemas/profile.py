from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

def to_camel(string: str) -> str:
    """Convert snake_case to camelCase"""
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

class CamelModel(BaseModel):
    """Base model that converts snake_case to camelCase"""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        by_alias=True
    )

# Profile Management Schemas
class ProfileUpdate(CamelModel):
    """Schema for updating user profile"""
    github_username: Optional[str] = None
    leetcode_username: Optional[str] = None
    geeksforgeeks_username: Optional[str] = None
    codechef_username: Optional[str] = None
    hackerrank_username: Optional[str] = None
    devpost_username: Optional[str] = None
    devto_username: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    
    # Personal Information
    full_name: Optional[str] = None
    gender: Optional[str] = None
    profile_picture_url: Optional[str] = None
    contact_number: Optional[str] = None
    bio: Optional[str] = None
    
    # Education
    college_name: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    current_year: Optional[str] = None
    graduation_year: Optional[int] = None
    
    # Skills
    skills: Optional[str] = None

class ProfileResponse(CamelModel):
    """Schema for profile response"""
    id: int
    user_id: int
    username: str
    name: str
    email: str
    github_username: Optional[str] = None
    leetcode_username: Optional[str] = None
    geeksforgeeks_username: Optional[str] = None
    codechef_username: Optional[str] = None
    hackerrank_username: Optional[str] = None
    devpost_username: Optional[str] = None
    devto_username: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    
    # Personal Information
    full_name: Optional[str] = None
    gender: Optional[str] = None
    profile_picture_url: Optional[str] = None
    contact_number: Optional[str] = None
    bio: Optional[str] = None
    
    # Education
    college_name: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    current_year: Optional[str] = None
    graduation_year: Optional[int] = None
    
    # Skills
    skills: Optional[str] = None
    
    created_at: datetime
    updated_at: Optional[datetime] = None

class PublicProfileResponse(CamelModel):
    """Schema for public profile (limited info)"""
    username: str
    name: str
    email: str  # Added email field
    github_username: Optional[str] = None
    leetcode_username: Optional[str] = None
    geeksforgeeks_username: Optional[str] = None
    codechef_username: Optional[str] = None
    hackerrank_username: Optional[str] = None
    devpost_username: Optional[str] = None
    devto_username: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    resume_url: Optional[str] = None
    
    # Personal Information
    full_name: Optional[str] = None
    gender: Optional[str] = None
    profile_picture_url: Optional[str] = None
    contact_number: Optional[str] = None
    bio: Optional[str] = None
    
    # Education
    college_name: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    current_year: Optional[str] = None
    graduation_year: Optional[int] = None
    
    # Skills
    skills: Optional[str] = None
    
    created_at: datetime

class ProfileRequest(BaseModel):
    github_username: Optional[str] = None
    leetcode_username: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_text: Optional[str] = None
    target_role: Optional[str] = "Software Engineer"

class PlatformMetric(CamelModel):
    name: str
    value: float

class PlatformScore(CamelModel):
    name: str
    score: float
    total: float = 100.0
    metrics: List[PlatformMetric]
    highlights: List[str]
    stats: Optional[Dict[str, Any]] = None

class MarketAnalysis(CamelModel):
    demand_score: float
    trending_skills: List[str]
    salary_estimate: str
    top_companies: List[str]

class Recommendation(CamelModel):
    title: str
    description: str
    priority: str
    category: str

class LearningResource(CamelModel):
    name: str
    url: str

class RoadmapPhase(CamelModel):
    phase: str
    tasks: List[str]
    resources: List[LearningResource]

class JobMatch(CamelModel):
    role: str
    fit_percent: float
    gaps: List[str]

class JobListing(CamelModel):
    title: str
    company: str
    location: str
    url: str
    match_score: float
    source: str

class AnalysisResponse(CamelModel):
    composite_score: float
    platform_scores: List[PlatformScore]
    market_analysis: MarketAnalysis
    recommendations: List[Recommendation]
    roadmap: List[RoadmapPhase]
    job_match: JobMatch
    job_listings: Optional[List[JobListing]] = []
