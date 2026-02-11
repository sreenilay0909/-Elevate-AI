"""Test personal information fields"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_profile_update():
    """Test updating profile with personal information"""
    
    # First, login to get token
    print("1. Logging in...")
    login_data = {
        "username": "sreenilay",
        "password": "your_password_here"  # Update with actual password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login successful")
    
    # Get current profile
    print("\n2. Getting current profile...")
    response = requests.get(f"{BASE_URL}/profiles/me", headers=headers)
    if response.status_code == 200:
        profile = response.json()
        print("✓ Current profile retrieved")
        print(f"   Username: {profile.get('username')}")
        print(f"   Full Name: {profile.get('fullName', 'Not set')}")
        print(f"   Bio: {profile.get('bio', 'Not set')}")
    
    # Update profile with personal information
    print("\n3. Updating profile with personal information...")
    update_data = {
        "fullName": "Madur Sree Nilay",
        "gender": "Male",
        "contactNumber": "+91 9876543210",
        "bio": "Passionate software developer with expertise in full-stack development. Love building scalable applications and solving complex problems.",
        "collegeName": "Indian Institute of Technology",
        "degree": "Bachelor's",
        "fieldOfStudy": "Computer Science and Engineering",
        "currentYear": "3rd Year",
        "graduationYear": 2026,
        "skills": "Python, JavaScript, React, Node.js, FastAPI, PostgreSQL, MongoDB, AWS, Docker, Git"
    }
    
    response = requests.put(f"{BASE_URL}/profiles/me", json=update_data, headers=headers)
    if response.status_code == 200:
        print("✓ Profile updated successfully")
        updated_profile = response.json()
        print(f"   Full Name: {updated_profile.get('fullName')}")
        print(f"   College: {updated_profile.get('collegeName')}")
        print(f"   Skills: {updated_profile.get('skills')}")
    else:
        print(f"❌ Update failed: {response.text}")
        return
    
    # Get public profile
    print("\n4. Getting public profile...")
    response = requests.get(f"{BASE_URL}/profiles/sreenilay")
    if response.status_code == 200:
        public_profile = response.json()
        print("✓ Public profile retrieved")
        print(f"   Full Name: {public_profile.get('fullName')}")
        print(f"   Gender: {public_profile.get('gender')}")
        print(f"   Bio: {public_profile.get('bio')[:50]}...")
        print(f"   College: {public_profile.get('collegeName')}")
        print(f"   Degree: {public_profile.get('degree')}")
        print(f"   Field: {public_profile.get('fieldOfStudy')}")
        print(f"   Year: {public_profile.get('currentYear')}")
        print(f"   Graduation: {public_profile.get('graduationYear')}")
        print(f"   Skills: {public_profile.get('skills')}")
    else:
        print(f"❌ Failed to get public profile: {response.text}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Personal Information Feature")
    print("=" * 60)
    test_profile_update()
