"""Test GeeksforGeeks API endpoints"""
import requests
import json

username = "sreenilay"

# Try different API endpoints
api_urls = [
    f"https://practiceapi.geeksforgeeks.org/api/vr/user-profile/profile/{username}/",
    f"https://practiceapi.geeksforgeeks.org/api/latest/user-profile/{username}/",
    f"https://auth.geeksforgeeks.org/api/profile/{username}/",
    f"https://www.geeksforgeeks.org/api/profile/{username}/",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

print(f"Testing API endpoints for user: {username}\n")

for url in api_urls:
    print(f"Trying: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  ✓ Got JSON response!")
                print(f"  Keys: {list(data.keys())[:10]}")
                
                # Save response
                filename = f"gfg_api_response_{api_urls.index(url)}.json"
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"  ✓ Saved to {filename}")
                
                # Look for relevant fields
                def find_keys(d, target_keys, prefix=''):
                    found = {}
                    if isinstance(d, dict):
                        for k, v in d.items():
                            full_key = f"{prefix}.{k}" if prefix else k
                            if any(target in k.lower() for target in ['score', 'problem', 'rank', 'article', 'streak', 'potd']):
                                found[full_key] = v
                            if isinstance(v, dict):
                                found.update(find_keys(v, target_keys, full_key))
                    return found
                
                relevant = find_keys(data, ['score', 'problem', 'rank', 'article', 'streak', 'potd'])
                if relevant:
                    print(f"  Relevant fields found:")
                    for k, v in list(relevant.items())[:10]:
                        print(f"    {k}: {v}")
                
                print()
                break
            except json.JSONDecodeError:
                print(f"  ✗ Not JSON")
        else:
            print(f"  ✗ Failed")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    print()

print("\n" + "="*60)
print("If no API worked, we'll need to use Selenium or find another approach")
