"""Test LinkedIn URL saving"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_linkedin_save():
    """Test saving LinkedIn URL"""
    
    # Login first
    print("1. Logging in...")
    login_data = {
        "username": "sreenilay",
        "password": "your_password_here"  # Replace with actual password
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return
    
    token = response.json()["accessToken"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")
    
    # Get current profile
    print("\n2. Getting current profile...")
    response = requests.get(f"{BASE_URL}/api/v1/profiles/me", headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to get profile: {response.text}")
        return
    
    profile = response.json()
    print(f"✅ Current profile:")
    print(f"   LinkedIn URL: {profile.get('linkedinUrl', 'Not set')}")
    
    # Update with LinkedIn URL
    print("\n3. Updating LinkedIn URL...")
    update_data = {
        "linkedinUrl": "https://www.linkedin.com/in/sreenilay"
    }
    
    response = requests.put(
        f"{BASE_URL}/api/v1/profiles/me",
        json=update_data,
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Update failed: {response.text}")
        return
    
    updated_profile = response.json()
    print(f"✅ Profile updated!")
    print(f"   LinkedIn URL: {updated_profile.get('linkedinUrl', 'Not set')}")
    
    # Verify by getting profile again
    print("\n4. Verifying update...")
    response = requests.get(f"{BASE_URL}/api/v1/profiles/me", headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to verify: {response.text}")
        return
    
    verified_profile = response.json()
    linkedin_url = verified_profile.get('linkedinUrl')
    
    if linkedin_url == "https://www.linkedin.com/in/sreenilay":
        print(f"✅ LinkedIn URL saved successfully!")
        print(f"   Verified: {linkedin_url}")
    else:
        print(f"❌ LinkedIn URL not saved correctly")
        print(f"   Expected: https://www.linkedin.com/in/sreenilay")
        print(f"   Got: {linkedin_url}")

if __name__ == "__main__":
    test_linkedin_save()
