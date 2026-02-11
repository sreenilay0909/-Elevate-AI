"""Test AI Analysis Endpoint"""
import requests
import json

# Base URL
BASE_URL = "http://127.0.0.1:8000"

# Login first to get token
print("1. Logging in...")
login_response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    json={
        "email_or_username": "sreenilay",
        "password": "Sreenilay@123"
    }
)

if login_response.status_code != 200:
    print(f"Login failed: {login_response.text}")
    exit(1)

token = login_response.json()["auth_token"]
print(f"✓ Logged in successfully")

# Set headers
headers = {
    "Authorization": f"Bearer {token}"
}

# Test AI analysis for GitHub
print("\n2. Testing AI analysis for GitHub...")
try:
    analysis_response = requests.get(
        f"{BASE_URL}/api/v1/ai/analyze/github",
        headers=headers
    )
    
    print(f"Status Code: {analysis_response.status_code}")
    
    if analysis_response.status_code == 200:
        analysis = analysis_response.json()
        print(f"✓ AI Analysis successful!")
        print(f"\nAnalysis Summary:")
        print(f"  Platform: {analysis['platform']}")
        print(f"  Username: {analysis['username']}")
        print(f"  Overall Score: {analysis['overallScore']}/100")
        print(f"  Percentile Rank: {analysis['percentileRank']}%")
        print(f"  Global Ranking: {analysis['globalRanking']}")
        print(f"\n  Strengths: {len(analysis['strengths'])} areas")
        print(f"  Weaknesses: {len(analysis['weaknesses'])} areas")
        print(f"  Recommendations: {len(analysis['recommendations'])} items")
        print(f"\n  First Strength: {analysis['strengths'][0]['topic']}")
        print(f"  First Recommendation: {analysis['recommendations'][0][:80]}...")
    else:
        print(f"✗ Error: {analysis_response.text}")
        
except Exception as e:
    print(f"✗ Exception: {e}")

# Test chat
print("\n3. Testing AI chat for GitHub...")
try:
    chat_response = requests.post(
        f"{BASE_URL}/api/v1/ai/chat/github",
        headers=headers,
        json={
            "question": "What should I focus on to improve my GitHub profile?",
            "chatHistory": []
        }
    )
    
    print(f"Status Code: {chat_response.status_code}")
    
    if chat_response.status_code == 200:
        chat = chat_response.json()
        print(f"✓ Chat successful!")
        print(f"\nAI Response:")
        print(f"  {chat['answer'][:200]}...")
    else:
        print(f"✗ Error: {chat_response.text}")
        
except Exception as e:
    print(f"✗ Exception: {e}")

print("\n✓ All tests completed!")
