"""Debug signup endpoint"""
import sys
import traceback
from app.db.database import SessionLocal
from app.models.user import User
from app.models.user_profile import UserProfile
from app.core.security import get_password_hash

try:
    db = SessionLocal()
    
    # Test creating a user
    print("Testing user creation...")
    
    new_user = User(
        email="debug@example.com",
        username="debuguser",
        password_hash=get_password_hash("Test123456"),
        name="Debug User",
        email_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"✅ User created: ID={new_user.id}, Email={new_user.email}")
    
    # Create profile
    user_profile = UserProfile(user_id=new_user.id)
    db.add(user_profile)
    db.commit()
    
    print(f"✅ Profile created for user {new_user.id}")
    
    db.close()
    print("\n✅ All tests passed!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
