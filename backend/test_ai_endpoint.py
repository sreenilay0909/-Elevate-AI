import requests

# Test if AI analysis endpoint exists
url = "http://127.0.0.1:8000/api/v1/ai/analyze/github"

# First, let's check what endpoints are available
docs_url = "http://127.0.0.1:8000/openapi.json"
response = requests.get(docs_url)

if response.status_code == 200:
    openapi = response.json()
    print("Available paths:")
    for path in openapi.get('paths', {}).keys():
        print(f"  {path}")
    
    # Check if our endpoint is there
    if '/api/v1/ai/analyze/{platform}' in openapi.get('paths', {}):
        print("\n✅ AI Analysis endpoint is registered!")
    else:
        print("\n❌ AI Analysis endpoint is NOT registered!")
else:
    print(f"Failed to get OpenAPI spec: {response.status_code}")
