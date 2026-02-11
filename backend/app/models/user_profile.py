"""User profile model for platform usernames"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class UserProfile(Base):
    """User profile with platform usernames"""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Platform usernames
    github_username = Column(String(100))
    leetcode_username = Column(String(100))
    geeksforgeeks_username = Column(String(100))
    codechef_username = Column(String(100))
    hackerrank_username = Column(String(100))
    devpost_username = Column(String(100))
    devto_username = Column(String(100))
    linkedin_url = Column(String(500))  # LinkedIn profile URL
    
    # Resume and portfolio
    resume_url = Column(String(500))
    portfolio_url = Column(String(500))
    
    # Personal Information
    full_name = Column(String(200))
    gender = Column(String(50))
    profile_picture_url = Column(String(500))
    contact_number = Column(String(20))
    bio = Column(String(1000))  # Self introduction
    
    # Education
    college_name = Column(String(200))
    degree = Column(String(200))
    field_of_study = Column(String(200))
    current_year = Column(String(50))  # e.g., "3rd Year", "Final Year"
    graduation_year = Column(Integer)
    
    # Skills
    skills = Column(String(1000))  # Comma-separated or JSON string
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile user_id={self.user_id}>"
