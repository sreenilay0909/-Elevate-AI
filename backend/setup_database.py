"""Setup script to initialize the database"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent))

from app.db.database import engine, Base
from app.models import User, UserProfile, EmailToken, PlatformData

def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print("\nTables created:")
    print("  - users")
    print("  - user_profiles")
    print("  - email_tokens")
    print("  - platform_data")

if __name__ == "__main__":
    init_db()
