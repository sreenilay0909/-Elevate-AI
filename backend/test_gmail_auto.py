"""Automated Gmail SMTP connection test"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.core.email import send_verification_email

async def test():
    """Test sending a verification email"""
    print("\n" + "="*60)
    print("Testing Gmail SMTP Connection")
    print("="*60)
    print("\nSending test verification email...")
    print("From: sreenilay0909@gmail.com")
    print("To: sreenilay0909@gmail.com (self-test)")
    
    try:
        await send_verification_email(
            to_email="sreenilay0909@gmail.com",
            name="Test User",
            code="123456"
        )
        print("\n✅ SUCCESS! Email sent successfully!")
        print("📧 Check your inbox: sreenilay0909@gmail.com")
        print("\nThe email should have:")
        print("  • Blue gradient header with 🚀 ElevateAI")
        print("  • Large 6-digit code: 123456")
        print("  • Professional layout with features section")
        print("  • 15-minute expiry notice")
        
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        print("\nPossible issues:")
        print("  • Check internet connection")
        print("  • Verify Gmail App Password is correct")
        print("  • Check if 2-Step Verification is enabled")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(test())
