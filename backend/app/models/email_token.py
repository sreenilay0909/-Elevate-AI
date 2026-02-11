"""Email verification token model"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class EmailToken(Base):
    """Email verification and password reset tokens"""
    __tablename__ = "email_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    token_type = Column(String(50), nullable=False)  # 'verification' or 'password_reset'
    
    # Verification code (6-digit number for email verification)
    code = Column(String(6), nullable=True, index=True)
    
    # Token status
    used = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="email_tokens")
    
    def __repr__(self):
        return f"<EmailToken {self.token_type} user_id={self.user_id}>"
