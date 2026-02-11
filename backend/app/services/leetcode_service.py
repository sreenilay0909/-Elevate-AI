import requests
from typing import Dict, Any, List

class LeetCodeService:
    BASE_URL = "https://leetcode.com/graphql"
    
    def analyze_profile(self, username: str) -> Dict[str, Any]:
        """Analyze LeetCode profile and return comprehensive metrics"""
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
                    reputation
                }
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
            
            if "errors" in data:
                raise Exception(f"LeetCode API error: {data['errors']}")
            
            if not data.get("data") or not data["data"].get("matchedUser"):
                raise Exception(f"LeetCode user '{username}' not found")
            
            user_data = data["data"]["matchedUser"]
            
            # Parse submissions
            submissions = {
                item["difficulty"]: item["count"]
                for item in user_data["submitStats"]["acSubmissionNum"]
            }
            
            easy = submissions.get("Easy", 0)
            medium = submissions.get("Medium", 0)
            hard = submissions.get("Hard", 0)
            total = easy + medium + hard
            
            # Get ranking
            ranking = user_data["profile"].get("ranking", 0)
            
            # Scoring
            problems_score = self._calculate_problems_score(easy, medium, hard)
            contest_score = self._calculate_contest_score(ranking)
            consistency_score = self._calculate_consistency_score(total)
            efficiency_score = self._calculate_efficiency_score(medium, hard, total)
            
            total_score = (
                problems_score * 0.35 +
                contest_score * 0.30 +
                consistency_score * 0.20 +
                efficiency_score * 0.15
            )
            
            return {
                "name": "LeetCode",
                "score": round(total_score, 2),
                "total": 100.0,
                "metrics": [
                    {"name": "Problems Solved", "value": round(problems_score, 2)},
                    {"name": "Contest Rating", "value": round(contest_score, 2)},
                    {"name": "Consistency", "value": round(consistency_score, 2)},
                    {"name": "Efficiency", "value": round(efficiency_score, 2)}
                ],
                "highlights": self._generate_highlights(total, easy, medium, hard, ranking),
                "stats": {
                    "username": username,
                    "total_solved": total,
                    "easy": easy,
                    "medium": medium,
                    "hard": hard,
                    "ranking": ranking,
                    "easy_percentage": round((easy / total * 100) if total > 0 else 0, 1),
                    "medium_percentage": round((medium / total * 100) if total > 0 else 0, 1),
                    "hard_percentage": round((hard / total * 100) if total > 0 else 0, 1)
                }
            }
        except requests.exceptions.Timeout:
            raise Exception("LeetCode API request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"LeetCode API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"LeetCode analysis failed: {str(e)}")
    
    def _calculate_problems_score(self, easy: int, medium: int, hard: int) -> float:
        """Calculate score based on problems solved with difficulty weighting"""
        # Weighted scoring: Easy=1, Medium=3, Hard=5
        weighted_score = (easy * 1 + medium * 3 + hard * 5)
        
        # Normalize to 100 scale (500 weighted problems = 100 score)
        score = min((weighted_score / 500) * 100, 100)
        
        return score
    
    def _calculate_contest_score(self, ranking: int) -> float:
        """Calculate score based on contest ranking"""
        if not ranking or ranking == 0:
            return 0
        
        # Top 1000 = 100, Top 10000 = 80, Top 100000 = 50, etc.
        if ranking <= 1000:
            return 100
        elif ranking <= 5000:
            return 90
        elif ranking <= 10000:
            return 80
        elif ranking <= 50000:
            return 60
        elif ranking <= 100000:
            return 40
        elif ranking <= 500000:
            return 20
        else:
            return 10
    
    def _calculate_consistency_score(self, total: int) -> float:
        """Calculate score based on total problems solved"""
        # 500 problems = 100 score
        score = min((total / 500) * 100, 100)
        return score
    
    def _calculate_efficiency_score(self, medium: int, hard: int, total: int) -> float:
        """Calculate score based on focus on harder problems"""
        if total == 0:
            return 0
        
        # Percentage of medium and hard problems
        hard_percentage = (medium + hard) / total
        
        # Higher percentage of hard problems = higher efficiency
        score = hard_percentage * 100
        
        # Bonus for solving many hard problems
        if hard > 100:
            score = min(score + 20, 100)
        elif hard > 50:
            score = min(score + 10, 100)
        
        return min(score, 100)
    
    def _generate_highlights(self, total: int, easy: int, medium: int, hard: int, ranking: int) -> List[str]:
        """Generate key highlights from the profile"""
        highlights = []
        
        if total > 1000:
            highlights.append(f"Solved {total}+ problems")
        elif total > 500:
            highlights.append(f"Solved {total} problems")
        elif total > 100:
            highlights.append(f"{total} problems solved")
        
        if hard > 100:
            highlights.append(f"Completed {hard}+ hard problems")
        elif hard > 50:
            highlights.append(f"{hard} hard problems solved")
        
        if medium > 300:
            highlights.append(f"Strong medium problem solver ({medium})")
        elif medium > 100:
            highlights.append(f"{medium} medium problems solved")
        
        if ranking and ranking > 0:
            if ranking <= 10000:
                highlights.append(f"Top {ranking:,} global ranking")
            elif ranking <= 100000:
                highlights.append(f"Ranked #{ranking:,} globally")
        
        # Problem distribution insight
        if total > 0:
            hard_ratio = hard / total
            if hard_ratio > 0.3:
                highlights.append("Strong focus on challenging problems")
            elif hard_ratio > 0.15:
                highlights.append("Balanced problem difficulty approach")
        
        if not highlights:
            highlights.append("Active on LeetCode")
        
        return highlights[:5]  # Return top 5 highlights
