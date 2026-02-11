"""LinkedIn service to add to platform_service_updated.py"""

class LinkedInService(BasePlatformService):
    """LinkedIn platform service
    
    Uses Playwright to extract public profile data from:
    https://www.linkedin.com/in/{username}
    
    Data fields:
    - Connections
    - Headline
    - Location
    - Experience Count
    - Education Count
    - Skills Count
    
    Note: LinkedIn has strict anti-scraping measures. This service
    extracts only publicly available information.
    """
    
    def get_platform_name(self) -> str:
        return "linkedin"
    
    def fetch_user_data(self, profile_url: str) -> Dict[str, Any]:
        """Fetch LinkedIn profile data using Playwright in subprocess
        
        Args:
            profile_url: Full LinkedIn profile URL (e.g., https://www.linkedin.com/in/username)
        """
        if not profile_url or not isinstance(profile_url, str):
            raise ValueError("Invalid LinkedIn URL")
        
        # Extract username from URL if full URL provided
        if 'linkedin.com/in/' in profile_url:
            username = profile_url.split('/in/')[-1].strip('/').split('?')[0]
        else:
            username = profile_url
        
        try:
            import subprocess
            import json
            import tempfile
            import os
            
            script = '''
import sys
import json
from playwright.sync_api import sync_playwright
import re

username = "''' + username + '''"
url = f"https://www.linkedin.com/in/{username}"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Set user agent to avoid detection
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()
        
        # Extract connections
        connections_patterns = [
            r'(\\d+)\\+?\\s*connections?',
            r'connections?[^\\d]*(\\d+)',
        ]
        connections = 0
        for pattern in connections_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                connections = int(match.group(1))
                break
        
        # Extract headline
        headline_match = re.search(r'<h2[^>]*>([^<]+)</h2>', content)
        headline = headline_match.group(1).strip() if headline_match else ""
        
        # Extract location
        location_match = re.search(r'location[^>]*>([^<]+)<', content, re.IGNORECASE)
        location = location_match.group(1).strip() if location_match else ""
        
        # Count experience entries
        experience_count = len(re.findall(r'experience', content, re.IGNORECASE))
        
        # Count education entries
        education_count = len(re.findall(r'education', content, re.IGNORECASE))
        
        # Count skills
        skills_match = re.search(r'(\\d+)\\s*skills?', content, re.IGNORECASE)
        skills_count = int(skills_match.group(1)) if skills_match else 0
        
        data = {
            'connections': connections,
            'headline': headline[:100] if headline else "Not available",
            'location': location[:50] if location else "Not available",
            'experience_count': min(experience_count, 20),  # Cap at reasonable number
            'education_count': min(education_count, 10),
            'skills_count': skills_count,
        }
        
        print(json.dumps(data))
except Exception as e:
    print(json.dumps({"error": str(e)}), file=sys.stderr)
    sys.exit(1)
'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(script)
                script_path = f.name
            
            try:
                result = subprocess.run(
                    ['python', script_path],
                    capture_output=True,
                    text=True,
                    timeout=40
                )
                
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    if 'error' in data:
                        raise ValueError(f"Playwright error: {data['error']}")
                    return data
                else:
                    raise ValueError(f"Script failed: {result.stderr}")
            finally:
                try:
                    os.unlink(script_path)
                except:
                    pass
                    
        except Exception as e:
            raise ValueError(f"Failed to fetch LinkedIn data: {str(e)}")
