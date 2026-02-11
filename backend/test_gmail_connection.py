"""Test Gmail SMTP connection and email sending"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.core.email import send_verification_email, send_password_reset_email, send_welcome_email

async def test_verification_email():
    """Test sending verification email"""
    print("\n" + "="*60)
    print("Testing Verification Email")
    print("="*60)
    
    test_email = input("\nEnter your email to receive test verification code: ").strip()
    test_name = input("Enter your name: ").strip() or "Test User"
    test_code = "123456"
    
    try:
        print("\nSending verification email...")
        await send_verification_email(test_email, test_name, test_code)
        print("✅ Verification email sent successfully!")
        print(f"📧 Check {test_email} for the email")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

async def test_password_reset_email():
    """Test sending password reset email"""
    print("\n" + "="*60)
    print("Testing Password Reset Email")
    print("="*60)
    
    test_email = input("\nEnter your email to receive test reset code: ").strip()
    test_name = input("Enter your name: ").strip() or "Test User"
    test_code = "654321"
    
    try:
        print("\nSending password reset email...")
        await send_password_reset_email(test_email, test_name, test_code)
        print("✅ Password reset email sent successfully!")
        print(f"📧 Check {test_email} for the email")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

async def test_welcome_email():
    """Test sending welcome email"""
    print("\n" + "="*60)
    print("Testing Welcome Email")
    print("="*60)
    
    test_email = input("\nEnter your email to receive welcome email: ").strip()
    test_name = input("Enter your name: ").strip() or "Test User"
    
    try:
        print("\nSending welcome email...")
        await send_welcome_email(test_email, test_name)
        print("✅ Welcome email sent successfully!")
        print(f"📧 Check {test_email} for the email")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

async def main():
    print("\n🧪 Gmail Email System Test")
    print("\nThis will test sending emails using Gmail SMTP")
    print("Email: sreenilay0909@gmail.com")
    print("\nChoose a test:")
    print("  1. Verification Email (with 6-digit code)")
    print("  2. Password Reset Email (with 6-digit code)")
    print("  3. Welcome Email")
    print("  4. All Three")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        await test_verification_email()
    elif choice == "2":
        await test_password_reset_email()
    elif choice == "3":
        await test_welcome_email()
    elif choice == "4":
        await test_verification_email()
        await test_password_reset_email()
        await test_welcome_email()
    else:
        print("Invalid choice!")
    
    print("\n" + "="*60)
    print("Test Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
