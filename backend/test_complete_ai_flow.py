"""
Complete test of AI Analysis flow
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Step 1: Login to get token
print("Step 1: Logging in...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email_or_username": "sreenilay009@gmail.com",  # Use your actual email
        "password": "MAXUR SREE NILAY"  # Use your actual password
    }
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.json())
    exit(1)

token = login_response.json()["access_token"]
print(f"✅ Login successful! Token: {token[:20]}...")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Step 2: Check if we have platform data
print("\nStep 2: Checking platform data...")
platform_data_response = requests.get(
    f"{BASE_URL}/platforms/data",
    headers=headers
)

if platform_data_response.status_code == 200:
    platforms = platform_data_response.json()
    print(f"✅ Found {len(platforms)} platforms with data")
    for p in platforms:
        print(f"  - {p['platform']}: {p['fetchStatus']}")
else:
    print(f"❌ Failed to get platform data: {platform_data_response.status_code}")
    print(platform_data_response.json())
    exit(1)

# Step 3: Test AI Analysis endpoint
if platforms:
    test_platform = platforms[0]['platform']
    print(f"\nStep 3: Testing AI Analysis for {test_platform}...")
    
    analysis_response = requests.get(
        f"{BASE_URL}/ai/analyze/{test_platform}",
        headers=headers
    )
    
    if analysis_response.status_code == 200:
        analysis = analysis_response.json()
        print(f"✅ AI Analysis successful!")
        print(f"  Percentile Rank: {analysis.get('percentileRank')}%")
        print(f"  Overall Score: {analysis.get('overallScore')}/100")
        print(f"  Global Ranking: {analysis.get('globalRanking')}")
        print(f"  Strengths: {len(analysis.get('strengths', []))}")
        print(f"  Weaknesses: {len(analysis.get('weaknesses', []))}")
        print(f"  Recommendations: {len(analysis.get('recommendations', []))}")
    else:
        print(f"❌ AI Analysis failed: {analysis_response.status_code}")
        print(analysis_response.json())
        
    # Step 4: Test Chat endpoint
    print(f"\nStep 4: Testing Chat for {test_platform}...")
    
    chat_response = requests.post(
        f"{BASE_URL}/ai/chat/{test_platform}",
        headers=headers,
        json={
            "question": "How can I improve my profile?",
            "chatHistory": []
        }
    )
    
    if chat_response.status_code == 200:
        chat = chat_response.json()
        print(f"✅ Chat successful!")
        print(f"  Answer: {chat.get('answer')[:100]}...")
    else:
        print(f"❌ Chat failed: {chat_response.status_code}")
        print(chat_response.json())
else:
    print("⚠️  No platform data available. Please fetch platform data first.")

print("\n" + "="*50)
print("Test complete!")
