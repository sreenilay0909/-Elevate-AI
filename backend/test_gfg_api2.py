"""Check the response from GFG API"""
import requests

username = "sreenilay"
url = f"https://www.geeksforgeeks.org/api/profile/{username}/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

response = requests.get(url, headers=headers, timeout=10)
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"\nFirst 1000 chars:")
print(response.text[:1000])

# Save full response
with open('gfg_api_response.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
print("\n✓ Full response saved to gfg_api_response.html")
