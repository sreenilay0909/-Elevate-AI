import google.generativeai as genai
from typing import Dict, Any, List
import json

class AIService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_recommendations(
        self, 
        platform_scores: List[Dict[str, Any]], 
        target_role: str
    ) -> Dict[str, Any]:
        """Generate AI-powered recommendations based on profile analysis"""
        
        # Prepare context for AI
        context = self._prepare_context(platform_scores, target_role)
        
        prompt = f"""
        Analyze this developer profile and provide career enhancement recommendations.
        
        Target Role: {target_role}
        
        Profile Analysis:
        {json.dumps(context, indent=2)}
        
        Please provide:
        1. Market analysis for the target role (trending skills, salary estimate, top companies)
        2. 3-5 specific recommendations with priority levels
        3. A 3-phase learning roadmap with specific tasks and resources
        4. Job match analysis (fit percentage and skill gaps)
        
        Format your response as JSON with this structure:
        {{
            "market_analysis": {{
                "demand_score": <number 0-100>,
                "trending_skills": [<list of 5-8 skills>],
                "salary_estimate": "<salary range>",
                "top_companies": [<list of 5-8 companies>]
            }},
            "recommendations": [
                {{
                    "title": "<recommendation title>",
                    "description": "<detailed description>",
                    "priority": "<High|Medium|Low>",
                    "category": "<Skill|Project|Certification|Networking>"
                }}
            ],
            "roadmap": [
                {{
                    "phase": "<phase name>",
                    "tasks": [<list of specific tasks>],
                    "resources": [
                        {{"name": "<resource name>", "url": "<url or placeholder>"}}
                    ]
                }}
            ],
            "job_match": {{
                "role": "{target_role}",
                "fit_percent": <number 0-100>,
                "gaps": [<list of missing skills/experience>]
            }}
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            ai_analysis = json.loads(response_text)
            
            return ai_analysis
            
        except json.JSONDecodeError as e:
            # Fallback to structured response if JSON parsing fails
            return self._generate_fallback_recommendations(platform_scores, target_role)
        except Exception as e:
            raise Exception(f"AI recommendation generation failed: {str(e)}")
    
    def _prepare_context(self, platform_scores: List[Dict[str, Any]], target_role: str) -> Dict[str, Any]:
        """Prepare context for AI analysis"""
        context = {
            "target_role": target_role,
            "platforms": []
        }
        
        for platform in platform_scores:
            platform_context = {
                "name": platform["name"],
                "score": platform["score"],
                "metrics": platform["metrics"],
                "highlights": platform["highlights"]
            }
            
            if "stats" in platform:
                platform_context["stats"] = platform["stats"]
            
            context["platforms"].append(platform_context)
        
        return context
    
    def _generate_fallback_recommendations(
        self, 
        platform_scores: List[Dict[str, Any]], 
        target_role: str
    ) -> Dict[str, Any]:
        """Generate fallback recommendations if AI fails"""
        
        # Calculate average score
        avg_score = sum(p["score"] for p in platform_scores) / len(platform_scores) if platform_scores else 0
        
        # Determine skill gaps based on scores
        weak_areas = [p["name"] for p in platform_scores if p["score"] < 60]
        
        return {
            "market_analysis": {
                "demand_score": 75,
                "trending_skills": [
                    "Python", "JavaScript", "React", "Node.js", 
                    "AWS", "Docker", "Kubernetes", "System Design"
                ],
                "salary_estimate": "$80,000 - $150,000",
                "top_companies": [
                    "Google", "Microsoft", "Amazon", "Meta", 
                    "Apple", "Netflix", "Uber", "Airbnb"
                ]
            },
            "recommendations": [
                {
                    "title": "Strengthen Coding Practice",
                    "description": "Increase problem-solving consistency on LeetCode. Focus on medium and hard problems.",
                    "priority": "High",
                    "category": "Skill"
                },
                {
                    "title": "Build Portfolio Projects",
                    "description": "Create 2-3 full-stack projects showcasing your skills in modern frameworks.",
                    "priority": "High",
                    "category": "Project"
                },
                {
                    "title": "Learn System Design",
                    "description": "Study system design patterns and architecture for senior-level interviews.",
                    "priority": "Medium",
                    "category": "Skill"
                }
            ],
            "roadmap": [
                {
                    "phase": "Foundation (Months 1-2)",
                    "tasks": [
                        "Solve 50 LeetCode problems (mix of easy and medium)",
                        "Complete a full-stack project using React and Node.js",
                        "Study data structures and algorithms"
                    ],
                    "resources": [
                        {"name": "LeetCode", "url": "https://leetcode.com"},
                        {"name": "FreeCodeCamp", "url": "https://freecodecamp.org"}
                    ]
                },
                {
                    "phase": "Intermediate (Months 3-4)",
                    "tasks": [
                        "Build a complex project with authentication and database",
                        "Learn cloud services (AWS/Azure basics)",
                        "Practice system design problems"
                    ],
                    "resources": [
                        {"name": "AWS Free Tier", "url": "https://aws.amazon.com/free"},
                        {"name": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer"}
                    ]
                },
                {
                    "phase": "Advanced (Months 5-6)",
                    "tasks": [
                        "Contribute to open source projects",
                        "Prepare for technical interviews",
                        "Network with industry professionals"
                    ],
                    "resources": [
                        {"name": "GitHub Explore", "url": "https://github.com/explore"},
                        {"name": "LinkedIn", "url": "https://linkedin.com"}
                    ]
                }
            ],
            "job_match": {
                "role": target_role,
                "fit_percent": min(avg_score, 100),
                "gaps": weak_areas if weak_areas else ["System Design", "Cloud Services"]
            }
        }
