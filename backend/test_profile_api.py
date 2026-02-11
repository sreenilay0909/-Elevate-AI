"""Test profile API endpoints"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_profile_endpoints():
    """Test profile management endpoints"""
    
    print("=" * 60)
    print("TESTING PROFILE API ENDPOINTS")
    print("=" * 60)
    
    # First, try to signup (or login if already exists)
    print("\n1. Creating test user...")
    signup_data = {
        "name": "Test User",
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "Test123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if response.status_code == 201:
            print("✓ User created successfully")
        elif response.status_code == 400:
            print("✓ User already exists, will login")
        else:
            print(f"Signup response: {response.status_code}")
    except Exception as e:
        print(f"Signup note: {e}")
    
    # Now login
    print("\n2. Logging in...")
    login_data = {
        "email_or_username": "testuser123",
        "password": "Test123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✓ Login successful")
            print(f"Token: {token[:20]}...")
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"✗ Login error: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test get my profile
    print("\n3. Getting my profile...")
    try:
        response = requests.get(f"{BASE_URL}/profiles/me", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print("✓ Profile retrieved successfully")
            print(f"Username: {profile.get('username')}")
            print(f"Name: {profile.get('name')}")
            print(f"Email: {profile.get('email')}")
        else:
            print(f"✗ Get profile failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Get profile error: {e}")
    
    # Test update profile
    print("\n4. Updating profile...")
    update_data = {
        "github_username": "testuser",
        "leetcode_username": "testuser",
        "portfolio_url": "https://testuser.dev"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/profiles/me", json=update_data, headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print("✓ Profile updated successfully")
            print(f"GitHub: {profile.get('githubUsername')}")
            print(f"LeetCode: {profile.get('leetcodeUsername')}")
            print(f"Portfolio: {profile.get('portfolioUrl')}")
        else:
            print(f"✗ Update profile failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Update profile error: {e}")
    
    # Test get public profile
    print("\n5. Getting public profile...")
    try:
        response = requests.get(f"{BASE_URL}/profiles/testuser123")
        if response.status_code == 200:
            profile = response.json()
            print("✓ Public profile retrieved successfully")
            print(f"Username: {profile.get('username')}")
            print(f"Name: {profile.get('name')}")
            print(f"GitHub: {profile.get('githubUsername')}")
        else:
            print(f"✗ Get public profile failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Get public profile error: {e}")
    
    print("\n" + "=" * 60)
    print("PROFILE API TESTING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_profile_endpoints()
