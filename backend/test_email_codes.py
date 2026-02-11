"""Test email verification code system"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1/auth"

def test_signup_and_verification():
    """Test signup and email verification with code"""
    
    print("\n" + "="*60)
    print("Testing Email Verification Code System")
    print("="*60)
    
    # Test data
    test_email = "testcode@example.com"
    test_username = "testcodeuser"
    test_password = "TestCode123"
    test_name = "Test Code User"
    
    # 1. Signup
    print("\n1. Testing Signup...")
    signup_data = {
        "email": test_email,
        "username": test_username,
        "password": test_password,
        "name": test_name
    }
    
    try:
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 201:
            print("   ✅ Signup successful!")
            print("   📧 Check console for verification code")
        else:
            print(f"   ❌ Signup failed: {response.json()}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 2. Get verification code from user
    print("\n2. Enter Verification Code")
    verification_code = input("   Enter the 6-digit code from console: ").strip()
    
    if len(verification_code) != 6 or not verification_code.isdigit():
        print("   ❌ Invalid code format. Must be 6 digits.")
        return
    
    # 3. Verify email
    print("\n3. Testing Email Verification...")
    verify_data = {
        "email": test_email,
        "code": verification_code
    }
    
    try:
        response = requests.post(f"{BASE_URL}/verify-email", json=verify_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Email verified successfully!")
        else:
            print(f"   ❌ Verification failed: {response.json()}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 4. Test login
    print("\n4. Testing Login...")
    login_data = {
        "email_or_username": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Login successful!")
            print(f"   User: {data['user']['name']} (@{data['user']['username']})")
            print(f"   Email Verified: {data['user']['email_verified']}")
        else:
            print(f"   ❌ Login failed: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*60)
    print("Test Complete!")
    print("="*60 + "\n")

def test_password_reset():
    """Test password reset with code"""
    
    print("\n" + "="*60)
    print("Testing Password Reset Code System")
    print("="*60)
    
    # Get email from user
    test_email = input("\nEnter email to reset password: ").strip()
    
    # 1. Request password reset
    print("\n1. Requesting Password Reset...")
    reset_request = {
        "email": test_email
    }
    
    try:
        response = requests.post(f"{BASE_URL}/forgot-password", json=reset_request)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Reset code sent!")
            print("   📧 Check console for reset code")
        else:
            print(f"   ❌ Request failed: {response.json()}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 2. Get reset code from user
    print("\n2. Enter Reset Code")
    reset_code = input("   Enter the 6-digit code from console: ").strip()
    
    if len(reset_code) != 6 or not reset_code.isdigit():
        print("   ❌ Invalid code format. Must be 6 digits.")
        return
    
    # 3. Get new password
    new_password = input("   Enter new password (min 8 chars, 1 upper, 1 lower, 1 number): ").strip()
    
    # 4. Reset password
    print("\n3. Resetting Password...")
    reset_data = {
        "email": test_email,
        "code": reset_code,
        "new_password": new_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/reset-password", json=reset_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Password reset successfully!")
        else:
            print(f"   ❌ Reset failed: {response.json()}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 5. Test login with new password
    print("\n4. Testing Login with New Password...")
    login_data = {
        "email_or_username": test_email,
        "password": new_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Login successful with new password!")
            print(f"   User: {data['user']['name']}")
        else:
            print(f"   ❌ Login failed: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*60)
    print("Test Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("\n🧪 Email Code System Test Suite")
    print("\nMake sure the backend is running:")
    print("  cd backend")
    print("  python -m uvicorn app.main:app --reload")
    print("\nChoose a test:")
    print("  1. Signup + Email Verification")
    print("  2. Password Reset")
    print("  3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_signup_and_verification()
    elif choice == "2":
        test_password_reset()
    elif choice == "3":
        test_signup_and_verification()
        input("\nPress Enter to continue to password reset test...")
        test_password_reset()
    else:
        print("Invalid choice!")
