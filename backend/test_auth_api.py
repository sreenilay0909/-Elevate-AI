"""Test script for authentication API"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1/auth"

def test_signup():
    """Test user signup"""
    print("\n=== Testing Signup ===")
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "Test123456",
        "name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/signup", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_login(email_or_username, password):
    """Test user login"""
    print("\n=== Testing Login ===")
    data = {
        "email_or_username": email_or_username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    return result

def test_get_current_user(token):
    """Test get current user"""
    print("\n=== Testing Get Current User ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get("http://127.0.0.1:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("🚀 Testing Authentication API")
    print("=" * 50)
    
    # Test health
    test_health()
    
    # Test signup
    try:
        signup_result = test_signup()
    except Exception as e:
        print(f"Signup error (might already exist): {e}")
    
    # Test login
    try:
        login_result = test_login("testuser", "Test123456")
        token = login_result.get("access_token")
        
        if token:
            # Test get current user
            test_get_current_user(token)
    except Exception as e:
        print(f"Login error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Testing Complete!")
    print("\nNext steps:")
    print("1. Open http://127.0.0.1:8000/docs to see Swagger UI")
    print("2. Test all endpoints interactively")
    print("3. Build frontend auth pages")
