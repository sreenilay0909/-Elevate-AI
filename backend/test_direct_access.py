import requests

# Try to access the endpoint directly
url = "http://127.0.0.1:8000/api/v1/ai/analyze/github"

# Without auth (should get 401)
response = requests.get(url)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

if response.status_code == 404:
    print("\n❌ Endpoint NOT FOUND (404)")
elif response.status_code == 401:
    print("\n✅ Endpoint EXISTS but requires authentication (401)")
elif response.status_code == 403:
    print("\n✅ Endpoint EXISTS but forbidden (403)")
else:
    print(f"\n⚠️  Unexpected status: {response.status_code}")
