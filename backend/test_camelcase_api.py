"""Test if API returns camelCase keys"""
import requests
import json

# Login first
login_response = requests.post(
    "http://127.0.0.1:8000/api/v1/auth/login",
    json={
        "email_or_username": "sreenilay0909@gmail.com",
        "password": "Sreenilay@123"
    }
)

if login_response.status_code == 200:
    token = login_response.json()["accessToken"]
    print("✓ Login successful")
    
    # Get platform data
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/platforms/data",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Got {len(data)} platforms\n")
        
        for platform in data:
            print(f"Platform: {platform['platform']}")
            print(f"Data keys: {list(platform['data'].keys())}")
            print(f"Sample data: {json.dumps(platform['data'], indent=2)[:200]}...")
            print("-" * 50)
    else:
        print(f"✗ Failed to get platform data: {response.status_code}")
        print(response.text)
else:
    print(f"✗ Login failed: {login_response.status_code}")
    print(login_response.text)
