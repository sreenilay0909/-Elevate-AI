"""AI Analysis Service for Platform Data"""
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from app.core.config import settings

class AIAnalysisService:
    """Service for AI-powered analysis of platform data"""
    
    def __init__(self):
        """Initialize AI Analysis Service with Gemini"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use gemini-flash-latest which is the stable latest flash model
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    def analyze_platform_data(
        self,
        platform: str,
        user_data: Dict[str, Any],
        username: str
    ) -> Dict[str, Any]:
        """
        Comprehensive AI analysis of platform data
        
        Args:
            platform: Platform name (github, leetcode, etc.)
            user_data: User's platform data
            username: User's username on the platform
            
        Returns:
            Complete analysis with ranking, strengths, weaknesses, and plan
        """
        
        # Generate analysis based on platform
        if platform == "github":
            return self._analyze_github(user_data, username)
        elif platform == "leetcode":
            return self._analyze_leetcode(user_data, username)
        elif platform == "geeksforgeeks":
            return self._analyze_geeksforgeeks(user_data, username)
        elif platform == "codechef":
            return self._analyze_codechef(user_data, username)
        elif platform == "hackerrank":
            return self._analyze_hackerrank(user_data, username)
        elif platform == "devpost":
            return self._analyze_devpost(user_data, username)
        elif platform == "devto":
            return self._analyze_devto(user_data, username)
        elif platform == "linkedin":
            return self._analyze_linkedin(user_data, username)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
    
    def _analyze_github(self, data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Analyze GitHub profile data"""
        
        prompt = f"""
Analyze this GitHub profile data and provide a comprehensive assessment:

Username: {username}
Public Repos: {data.get('publicRepos', 0)}
Followers: {data.get('followers', 0)}
Following: {data.get('following', 0)}
Total Stars: {data.get('totalStars', 0)}
Total Forks: {data.get('totalForks', 0)}
Contributions (Last Year): {data.get('contributionsLastYear', 0)}
Top Languages: {', '.join(data.get('topLanguages', [])[:5])}

Provide analysis in this exact JSON format:
{{
    "percentileRank": <number 0-100>,
    "globalRanking": "<description of where user stands>",
    "overallScore": <number 0-100>,
    "strengths": [
        {{"topic": "<strength area>", "score": <0-100>, "description": "<why it's strong>"}}
    ],
    "weaknesses": [
        {{"topic": "<weakness area>", "score": <0-100>, "description": "<why it needs improvement>"}}
    ],
    "recommendations": [
        "<specific actionable recommendation>"
    ],
    "weeklyPlan": {{
        "day1": "<specific task>",
        "day2": "<specific task>",
        "day3": "<specific task>",
        "day4": "<specific task>",
        "day5": "<specific task>",
        "day6": "<specific task>",
        "day7": "<specific task>"
    }},
    "keyMetrics": [
        {{"name": "<metric name>", "value": "<value>", "benchmark": "<industry benchmark>", "status": "good|average|needs_improvement"}}
    ]
}}

Base percentile ranking on:
- Contribution frequency and consistency
- Repository quality (stars, forks)
- Community engagement (followers)
- Language diversity
- Project impact

Provide 3-5 strengths and weaknesses each. Make recommendations specific and actionable.
"""
        
        response = self.model.generate_content(prompt)
        
        # Parse JSON from response
        response_text = response.text
        # Remove markdown code blocks if present
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        analysis = json.loads(response_text)
        analysis["platform"] = "github"
        analysis["username"] = username
        analysis["analyzedAt"] = datetime.utcnow().isoformat()
        
        return analysis
    
    def _analyze_leetcode(self, data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Analyze LeetCode profile data"""
        
        prompt = f"""
Analyze this LeetCode profile data and provide a comprehensive assessment:

Username: {username}
Total Solved: {data.get('totalSolved', 0)}
Easy Solved: {data.get('easySolved', 0)}
Medium Solved: {data.get('mediumSolved', 0)}
Hard Solved: {data.get('hardSolved', 0)}
Acceptance Rate: {data.get('acceptanceRate', 0)}%
Ranking: {data.get('ranking', 'N/A')}
Reputation: {data.get('reputation', 0)}
Contest Rating: {data.get('contestRating', 'N/A')}
Contest Attended: {data.get('contestsAttended', 0)}

Provide analysis in this exact JSON format:
{{
    "percentileRank": <number 0-100>,
    "globalRanking": "<description of where user stands>",
    "overallScore": <number 0-100>,
    "strengths": [
        {{"topic": "<strength area>", "score": <0-100>, "description": "<why it's strong>"}}
    ],
    "weaknesses": [
        {{"topic": "<weakness area>", "score": <0-100>, "description": "<why it needs improvement>"}}
    ],
    "recommendations": [
        "<specific actionable recommendation>"
    ],
    "weeklyPlan": {{
        "day1": "<specific task with problem types>",
        "day2": "<specific task with problem types>",
        "day3": "<specific task with problem types>",
        "day4": "<specific task with problem types>",
        "day5": "<specific task with problem types>",
        "day6": "<specific task with problem types>",
        "day7": "<specific task with problem types>"
    }},
    "keyMetrics": [
        {{"name": "<metric name>", "value": "<value>", "benchmark": "<industry benchmark>", "status": "good|average|needs_improvement"}}
    ],
    "topicBreakdown": [
        {{"topic": "<algorithm/data structure>", "solved": <number>, "total": <number>, "proficiency": <0-100>}}
    ]
}}

Base percentile ranking on:
- Total problems solved
- Difficulty distribution (hard problems weighted more)
- Contest performance
- Acceptance rate
- Consistency

Provide specific problem-solving strategies and focus areas.
"""
        
        response = self.model.generate_content(prompt)
        
        # Parse JSON from response
        response_text = response.text
        # Remove markdown code blocks if present
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        analysis = json.loads(response_text)
        analysis["platform"] = "leetcode"
        analysis["username"] = username
        analysis["analyzedAt"] = datetime.utcnow().isoformat()
        
        return analysis
    
    def _analyze_geeksforgeeks(self, data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Analyze GeeksforGeeks profile data"""
        
        prompt = f"""
Analyze this GeeksforGeeks profile data:

Username: {username}
Score: {data.get('score', 0)}
Problems Solved: {data.get('problemsSolved', 0)}
Coding Score: {data.get('codingScore', 0)}
Monthly Rank: {data.get('monthlyRank', 'N/A')}
Articles Published: {data.get('articlesPublished', 0)}

Provide comprehensive analysis in JSON format with percentileRank, globalRanking, overallScore, strengths, weaknesses, recommendations, weeklyPlan, and keyMetrics.
"""
        
        return self._get_ai_analysis(prompt, "geeksforgeeks", username)
    
    def _analyze_codechef(self, data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Analyze CodeChef profile data"""
        
        prompt = f"""
Analyze this CodeChef profile data:

Username: {username}
Rating: {data.get('rating', 0)}
Stars: {data.get('stars', 'N/A')}
Global Rank: {data.get('globalRank', 'N/A')}
Country Rank: {data.get('countryRank', 'N/A')}
Problems Solved: {data.get('problemsSolved', 0)}
Contests: {data.get('contests', 0)}

Provide comprehensive analysis in JSON format with percentileRank, globalRanking, overallScore, strengths, weaknesses, recommendations, weeklyPlan, and keyMetrics.
"""
        
        return self._get_ai_analysis(prompt, "codechef", username)
    
    def _analyze_hackerrank(self, data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Analyze HackerRank profile data"""
        
        prompt = f"""
Analyze this HackerRank profile data:

Username: {username}
Badges: {', '.join(data.get('badges', []))}
Challenges Solved: {data.get('challengesSolved', 0)}
Rank: {data.get('rank', 'N/A')}
Skills: {', '.join(data.get('skills', []))}

Provide comprehensive analysis in JSON format with percentileRank, globalRanking, overallScore, strengths, weaknesses, recommendations, weeklyPlan, and keyMetrics.
"""
        
        return self._get_ai_analysis(prompt, "hackerrank", username)
    
    def _analyze_devpost(self, data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Analyze DevPost profile data"""
        
        prompt = f"""
Analyze this DevPost profile data:

Username: {username}
Projects: {data.get('projects', 0)}
Hackathons: {data.get('hackathons', 0)}
Wins: {data.get('wins', 0)}
Likes: {data.get('likes', 0)}
Skills: {', '.join(data.get('skills', []))}

Provide comprehensive analysis in JSON format with percentileRank, globalRanking, overallScore, strengths, weaknesses, recommendations, weeklyPlan, and keyMetrics.
"""
        
        return self._get_ai_analysis(prompt, "devpost", username)
    
    def _analyze_devto(self, data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Analyze Dev.to profile data"""
        
        prompt = f"""
Analyze this Dev.to profile data:

Username: {username}
Posts: {data.get('posts', 0)}
Followers: {data.get('followers', 0)}
Post Reactions: {data.get('postReactions', 0)}
Comments: {data.get('comments', 0)}
Tags: {', '.join(data.get('tags', []))}

Provide comprehensive analysis in JSON format with percentileRank, globalRanking, overallScore, strengths, weaknesses, recommendations, weeklyPlan, and keyMetrics.
"""
        
        return self._get_ai_analysis(prompt, "devto", username)
    
    def _analyze_linkedin(self, data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Analyze LinkedIn profile data"""
        
        prompt = f"""
Analyze this LinkedIn profile data:

Name: {data.get('name', 'N/A')}
Headline: {data.get('headline', 'N/A')}
Connections: {data.get('connections', 0)}
Experience: {data.get('experienceYears', 0)} years
Skills: {', '.join(data.get('skills', [])[:10])}
Endorsements: {data.get('endorsements', 0)}

Provide comprehensive analysis in JSON format with percentileRank, globalRanking, overallScore, strengths, weaknesses, recommendations, weeklyPlan, and keyMetrics.
"""
        
        return self._get_ai_analysis(prompt, "linkedin", username)
    
    def _get_ai_analysis(self, prompt: str, platform: str, username: str) -> Dict[str, Any]:
        """Generic AI analysis helper"""
        
        response = self.model.generate_content(prompt)
        
        # Parse JSON from response
        response_text = response.text
        # Remove markdown code blocks if present
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        analysis = json.loads(response_text)
        analysis["platform"] = platform
        analysis["username"] = username
        analysis["analyzedAt"] = datetime.utcnow().isoformat()
        
        return analysis
    
    def chat_with_platform_context(
        self,
        platform: str,
        user_data: Dict[str, Any],
        analysis: Dict[str, Any],
        question: str,
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Platform-specific Q&A chatbot with enhanced context awareness
        
        Args:
            platform: Platform name
            user_data: User's platform data
            analysis: Previous analysis results
            question: User's question
            chat_history: Previous chat messages
            
        Returns:
            AI response specific to the platform
        """
        
        if chat_history is None:
            chat_history = []
        
        # Get platform-specific context
        platform_contexts = {
            "github": "GitHub profile optimization, repository management, contribution strategies, open source collaboration, and code quality",
            "leetcode": "LeetCode problem-solving strategies, algorithm patterns, data structures, contest preparation, and coding interview techniques",
            "geeksforgeeks": "GeeksforGeeks practice problems, competitive programming, DSA concepts, and technical interview preparation",
            "codechef": "CodeChef contest strategies, competitive programming techniques, rating improvement, and problem-solving approaches",
            "hackerrank": "HackerRank skill development, certification preparation, domain-specific challenges, and technical assessments",
            "devpost": "Hackathon participation, project showcasing, team collaboration, and innovation strategies",
            "devto": "Technical blogging, community engagement, content creation, and developer networking",
            "linkedin": "Professional networking, profile optimization, career development, and industry connections"
        }
        
        platform_context = platform_contexts.get(platform, f"{platform} performance optimization")
        
        # Build enhanced context
        context = f"""
You are an expert {platform.upper()} advisor specializing in {platform_context}.

CRITICAL RULES:
1. You MUST ONLY discuss {platform.upper()} topics
2. If the user asks about other platforms or unrelated topics, politely say: "I'm specialized in {platform.upper()} only. For that topic, please use the relevant platform's AI assistant."
3. Always reference the user's actual data when giving advice
4. Provide specific, actionable steps (not generic advice)
5. Be encouraging and supportive
6. Use numbers and metrics from their data
7. Keep responses concise (2-4 paragraphs max)

USER'S {platform.upper()} DATA:
{json.dumps(user_data, indent=2)}

ANALYSIS SUMMARY:
- Overall Score: {analysis.get('overallScore', 'N/A')}/100
- Percentile Rank: {analysis.get('percentileRank', 'N/A')}%
- Top Strength: {analysis.get('strengths', [{}])[0].get('topic', 'N/A') if analysis.get('strengths') else 'N/A'}
- Main Weakness: {analysis.get('weaknesses', [{}])[0].get('topic', 'N/A') if analysis.get('weaknesses') else 'N/A'}

RECENT CONVERSATION:
{json.dumps(chat_history[-3:], indent=2) if chat_history else 'No previous messages'}

USER'S QUESTION: {question}

Provide a helpful, specific answer that:
- Directly addresses their question
- References their actual {platform.upper()} data
- Gives actionable next steps
- Stays focused on {platform.upper()} only
"""
        
        response = self.model.generate_content(context)
        return response.text
