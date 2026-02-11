"""Platform data cache model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class PlatformData(Base):
    """Cached platform data for users"""
    __tablename__ = "platform_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform_name = Column(String(50), nullable=False)
    
    # Cached data
    data = Column(JSON, nullable=False)
    
    # Update tracking
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    next_update = Column(DateTime(timezone=True))
    update_status = Column(String(50), default="success")  # success, failed, pending
    error_message = Column(String(500))
    
    # Relationships
    user = relationship("User", back_populates="platform_data")
    
    # Unique constraint on user_id and platform_name
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )
    
    def __repr__(self):
        return f"<PlatformData {self.platform_name} user_id={self.user_id}>"
