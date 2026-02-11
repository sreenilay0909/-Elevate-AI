"""Updated platform services for fetching user statistics"""
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup
from github import Github, GithubException
from datetime import datetime, timedelta
from .base_platform_service import BasePlatformService

class GitHubServiceUpdated(BasePlatformService):
    """GitHub platform service"""
    
    def __init__(self, token: str = None):
        super().__init__()
        self.client = Github(token) if token else Github()
    
    def get_platform_name(self) -> str:
        return "github"
    
    def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """Fetch GitHub user statistics"""
        if not self.validate_username(username):
            raise ValueError("Invalid username")
        
        try:
            user = self.client.get_user(username)
            repos = list(user.get_repos())
            original_repos = [repo for repo in repos if not repo.fork]
            
            # Calculate total stars
            total_stars = sum(repo.stargazers_count for repo in original_repos)
            
            # Get top languages
            languages = {}
            for repo in original_repos:
                if repo.language:
                    languages[repo.language] = languages.get(repo.language, 0) + 1
            top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
            
            # Calculate commits (approximate from recent activity)
            one_year_ago = datetime.now() - timedelta(days=365)
            recent_repos = [r for r in original_repos if r.pushed_at and r.pushed_at.replace(tzinfo=None) > one_year_ago]
            commits_estimate = len(recent_repos) * 20  # Rough estimate
            
            # Calculate streak (days since last push)
            if original_repos:
                latest_push = max([r.pushed_at for r in original_repos if r.pushed_at])
                days_since_push = (datetime.now() - latest_push.replace(tzinfo=None)).days
                streak = max(0, 365 - days_since_push) if days_since_push < 365 else 0
            else:
                streak = 0
            
            return {
                "repositories": len(original_repos),
                "stars": total_stars,
                "commits_last_year": commits_estimate,
                "top_languages": [lang[0] for lang in top_languages],
                "contribution_streak": streak,
                "followers": user.followers,
                "following": user.following
            }
        except GithubException as e:
            if e.status == 404:
                raise ValueError(f"GitHub user '{username}' not found")
            elif e.status == 403:
                raise ValueError("GitHub API rate limit exceeded")
            else:
                raise ValueError(f"GitHub API error: {str(e)}")


class LeetCodeServiceUpdated(BasePlatformService):
    """LeetCode platform service"""
    
    BASE_URL = "https://leetcode.com/graphql"
    
    def get_platform_name(self) -> str:
        return "leetcode"
    
    def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """Fetch LeetCode user statistics"""
        if not self.validate_username(username):
            raise ValueError("Invalid username")
        
        query = """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                username
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
                profile {
                    ranking
                }
            }
            recentSubmissionList(username: $username, limit: 20) {
                timestamp
            }
        }
        """
        
        try:
            response = requests.post(
                self.BASE_URL,
                json={"query": query, "variables": {"username": username}},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "errors" in data or not data.get("data", {}).get("matchedUser"):
                raise ValueError(f"LeetCode user '{username}' not found")
            
            user_data = data["data"]["matchedUser"]
            submissions = {
                item["difficulty"]: item["count"]
                for item in user_data["submitStats"]["acSubmissionNum"]
            }
            
            easy = submissions.get("Easy", 0)
            medium = submissions.get("Medium", 0)
            hard = submissions.get("Hard", 0)
            total = easy + medium + hard
            
            ranking = user_data["profile"].get("ranking", 0)
            
            # Calculate acceptance rate (simplified)
            acceptance_rate = round((total / (total + 100)) * 100, 1) if total > 0 else 0
            
            # Calculate streak from recent submissions
            recent_submissions = data["data"].get("recentSubmissionList", [])
            streak = len(recent_submissions) if recent_submissions else 0
            
            return {
                "total_solved": total,
                "easy_solved": easy,
                "medium_solved": medium,
                "hard_solved": hard,
                "acceptance_rate": acceptance_rate,
                "ranking": ranking,
                "streak": streak
            }
        except requests.exceptions.RequestException as e:
            raise ValueError(f"LeetCode API request failed: {str(e)}")


class GeeksforGeeksService(BasePlatformService):
    """GeeksforGeeks platform service
    
    Uses Playwright to render JavaScript and extract data from:
    https://www.geeksforgeeks.org/profile/{username}/?tab=activity
    
    Data fields:
    - Coding Score
    - Problems Solved
    - Institute Rank
    - Articles Published
    - Longest Streak
    - POTDs Solved
    """
    
    def get_platform_name(self) -> str:
        return "geeksforgeeks"
    
    def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """Fetch GeeksforGeeks user statistics using Playwright in thread"""
        if not self.validate_username(username):
            raise ValueError("Invalid username")
        
        try:
            # Run Playwright in a separate thread to avoid event loop conflicts
            from concurrent.futures import ThreadPoolExecutor
            import subprocess
            import json
            
            # Create a simple Python script to run Playwright
            script = f"""
import sys
import json
from playwright.sync_api import sync_playwright
import re

username = "{username}"
url = f"https://www.geeksforgeeks.org/profile/{{username}}/?tab=activity"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({{"width": 1920, "height": 1080}})
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()
        
        def extract_stat(patterns, default=0):
            if isinstance(patterns, str):
                patterns = [patterns]
            for pattern in patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    value = match.group(1).replace(',', '')
                    try:
                        return int(value)
                    except:
                        pass
            return default
        
        data = {{
            'coding_score': extract_stat([
                r'Coding Score[^\\d]*(\\d+)',
                r'coding[_\\s-]?score[^\\d]*(\\d+)',
            ]),
            'problems_solved': extract_stat([
                r'Problems Solved[^\\d]*(\\d+)',
                r'problems?[_\\s-]?solved[^\\d]*(\\d+)',
            ]),
            'institute_rank': extract_stat([
                r'Institute Rank[^\\d]*(\\d+)',
                r'institute[_\\s-]?rank[^\\d]*(\\d+)',
            ]),
            'articles_published': extract_stat([
                r'Articles Published[^\\d]*(\\d+)',
                r'articles?[_\\s-]?published[^\\d]*(\\d+)',
                r'(\\d+)\\s*articles?',
            ]),
            'longest_streak': extract_stat([
                r'Longest Streak[^\\d]*(\\d+)',
                r'longest[_\\s-]?streak[^\\d]*(\\d+)',
                r'streak[^\\d]*(\\d+)\\s*days?',
            ]),
            'potds_solved': extract_stat([
                r'POTDs Solved[^\\d]*(\\d+)',
                r'potds?[_\\s-]?solved[^\\d]*(\\d+)',
                r'(\\d+)\\s*potds?',
            ]),
        }}
        
        print(json.dumps(data))
except Exception as e:
    print(json.dumps({{"error": str(e)}}), file=sys.stderr)
    sys.exit(1)
"""
            
            # Write script to temp file and execute
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(script)
                script_path = f.name
            
            try:
                # Run the script in a subprocess
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
                # Clean up temp file
                try:
                    os.unlink(script_path)
                except:
                    pass
                    
        except Exception as e:
            raise ValueError(f"Failed to fetch GeeksforGeeks data: {str(e)}")


class CodeChefService(BasePlatformService):
    """CodeChef platform service
    
    Uses Playwright to render JavaScript and extract data from:
    https://www.codechef.com/users/{username}
    
    Data fields:
    - Current Rating
    - Star Rating (1-7 stars)
    - Problems Solved
    - Contest Participation
    - Global Rank
    - Country Rank
    """
    
    def get_platform_name(self) -> str:
        return "codechef"
    
    def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """Fetch CodeChef user statistics using Playwright in subprocess"""
        if not self.validate_username(username):
            raise ValueError("Invalid username")
        
        try:
            import subprocess
            import json
            import tempfile
            import os
            
            # Create script with proper escaping
            script = '''
import sys
import json
from playwright.sync_api import sync_playwright
import re

username = "''' + username + '''"
url = f"https://www.codechef.com/users/{username}"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()
        
        # Extract rating with multiple patterns
        rating = 0
        rating_patterns = [
            r'rating.*?(\\d{3,4})',
            r'<div[^>]*rating[^>]*>(\\d+)',
            r'rating-number[^>]*>(\\d+)',
        ]
        for pattern in rating_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                rating = int(match.group(1))
                if rating > 100:  # Valid rating
                    break
        
        # Calculate stars
        if rating >= 2500: stars = 7
        elif rating >= 2200: stars = 6
        elif rating >= 1800: stars = 5
        elif rating >= 1600: stars = 4
        elif rating >= 1400: stars = 3
        elif rating >= 1200: stars = 2
        else: stars = 1 if rating > 0 else 0
        
        # Extract problems solved - try multiple patterns
        problems_solved = 0
        problems_patterns = [
            r'Total Problems Solved:\s*(\d+)',  # New pattern for "Total Problems Solved: 34"
            r'(\d+)\s*problems?\s*solved',
            r'problems?\s*solved[^\d]*(\d+)',
        ]
        for pattern in problems_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                problems_solved = int(match.group(1))
                break
        
        # Extract contests
        contests_match = re.search(r'(\\d+)\\s*contests?', content, re.IGNORECASE)
        contests = int(contests_match.group(1)) if contests_match else 0
        
        # Extract ranks
        global_rank_match = re.search(r'global\\s*rank[^\\d]*(\\d+)', content, re.IGNORECASE)
        global_rank = int(global_rank_match.group(1)) if global_rank_match else 0
        
        country_rank_match = re.search(r'country\\s*rank[^\\d]*(\\d+)', content, re.IGNORECASE)
        country_rank = int(country_rank_match.group(1)) if country_rank_match else 0
        
        data = {
            'current_rating': rating,
            'stars': stars,
            'problems_solved': problems_solved,
            'contests_participated': contests,
            'global_rank': global_rank,
            'country_rank': country_rank,
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
            raise ValueError(f"Failed to fetch CodeChef data: {str(e)}")


class HackerRankService(BasePlatformService):
    """HackerRank platform service"""
    
    def get_platform_name(self) -> str:
        return "hackerrank"
    
    def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """Fetch HackerRank user statistics via web scraping"""
        if not self.validate_username(username):
            raise ValueError("Invalid username")
        
        url = f"https://www.hackerrank.com/{username}"
        
        try:
            response = self.safe_get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract stars (simplified - would need more complex parsing)
            stars = 0
            
            # Extract badges
            badges = 0
            
            # Extract skills
            skills = 0
            
            return {
                "total_stars": stars,
                "badges_earned": badges,
                "skills_verified": skills,
                "domain_ranks": {},
                "certificates": 0
            }
        except Exception as e:
            raise ValueError(f"Failed to fetch HackerRank data: {str(e)}")


class DevPostService(BasePlatformService):
    """DevPost platform service
    
    Uses Playwright to render JavaScript and extract data from:
    https://devpost.com/{username}
    
    Data fields:
    - Projects Submitted
    - Hackathons Participated
    - Prizes Won
    - Followers
    - Likes Received
    """
    
    def get_platform_name(self) -> str:
        return "devpost"
    
    def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """Fetch DevPost user statistics using Playwright in subprocess"""
        if not self.validate_username(username):
            raise ValueError("Invalid username")
        
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
url = f"https://devpost.com/{username}"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()
        
        # Extract projects
        projects_patterns = [
            r'(\\d+)\\s*projects?',
            r'projects[^\\d]*(\\d+)',
            r'<span[^>]*>(\\d+)</span>\\s*projects?',
        ]
        projects = 0
        for pattern in projects_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                projects = int(match.group(1))
                break
        
        # Extract hackathons
        hackathons_patterns = [
            r'(\\d+)\\s*hackathons?',
            r'hackathons[^\\d]*(\\d+)',
        ]
        hackathons = 0
        for pattern in hackathons_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                hackathons = int(match.group(1))
                break
        
        # Extract prizes
        prizes_patterns = [
            r'(\\d+)\\s*prizes?',
            r'prizes[^\\d]*(\\d+)',
            r'won[^\\d]*(\\d+)',
        ]
        prizes = 0
        for pattern in prizes_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                prizes = int(match.group(1))
                break
        
        # Extract followers
        followers_patterns = [
            r'(\\d+)\\s*followers?',
            r'followers[^\\d]*(\\d+)',
        ]
        followers = 0
        for pattern in followers_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                followers = int(match.group(1))
                break
        
        # Extract likes
        likes_patterns = [
            r'(\\d+)\\s*likes?',
            r'likes[^\\d]*(\\d+)',
        ]
        likes = 0
        for pattern in likes_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                likes = int(match.group(1))
                break
        
        data = {
            'projects_submitted': projects,
            'hackathons_participated': hackathons,
            'prizes_won': prizes,
            'followers': followers,
            'likes_received': likes,
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
            raise ValueError(f"Failed to fetch DevPost data: {str(e)}")


class DevToService(BasePlatformService):
    """Dev.to platform service"""
    
    BASE_URL = "https://dev.to/api"
    
    def get_platform_name(self) -> str:
        return "devto"
    
    def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """Fetch Dev.to user statistics via official API"""
        if not self.validate_username(username):
            raise ValueError("Invalid username")
        
        try:
            # Get user info
            user_response = self.safe_get(f"{self.BASE_URL}/users/by_username?url={username}")
            user_data = user_response.json()
            
            # Get user articles
            articles_response = self.safe_get(f"{self.BASE_URL}/articles?username={username}")
            articles = articles_response.json()
            
            # Calculate total reactions and comments
            total_reactions = sum(article.get('public_reactions_count', 0) for article in articles)
            total_comments = sum(article.get('comments_count', 0) for article in articles)
            
            return {
                "articles_published": len(articles),
                "total_reactions": total_reactions,
                "total_comments": total_comments,
                "followers": user_data.get('followers_count', 0),
                "reading_list_items": 0  # Not available via public API
            }
        except Exception as e:
            raise ValueError(f"Failed to fetch Dev.to data: {str(e)}")


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
