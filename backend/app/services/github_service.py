from github import Github, GithubException
from typing import Dict, Any, List
from datetime import datetime, timedelta
import statistics

class GitHubService:
    def __init__(self, token: str = None):
        self.client = Github(token) if token else Github()
    
    def analyze_profile(self, username: str) -> Dict[str, Any]:
        """Analyze GitHub profile and return comprehensive metrics"""
        try:
            user = self.client.get_user(username)
            repos = list(user.get_repos())
            
            # Filter out forked repos for more accurate analysis
            original_repos = [repo for repo in repos if not repo.fork]
            
            # Calculate metrics
            total_stars = sum(repo.stargazers_count for repo in original_repos)
            total_forks = sum(repo.forks_count for repo in original_repos)
            
            # Language distribution
            languages = {}
            for repo in original_repos:
                if repo.language:
                    languages[repo.language] = languages.get(repo.language, 0) + 1
            
            # Recent activity (last 6 months)
            six_months_ago = datetime.now() - timedelta(days=180)
            recent_repos = [r for r in original_repos if r.pushed_at and r.pushed_at.replace(tzinfo=None) > six_months_ago]
            
            # Scoring
            code_quality_score = self._calculate_code_quality(original_repos)
            activity_score = self._calculate_activity(user, recent_repos, original_repos)
            impact_score = self._calculate_impact(total_stars, total_forks, user.followers)
            diversity_score = self._calculate_diversity(languages)
            
            total_score = (
                code_quality_score * 0.3 +
                activity_score * 0.25 +
                impact_score * 0.25 +
                diversity_score * 0.2
            )
            
            return {
                "name": "GitHub",
                "score": round(total_score, 2),
                "total": 100.0,
                "metrics": [
                    {"name": "Code Quality", "value": round(code_quality_score, 2)},
                    {"name": "Activity", "value": round(activity_score, 2)},
                    {"name": "Impact", "value": round(impact_score, 2)},
                    {"name": "Diversity", "value": round(diversity_score, 2)}
                ],
                "highlights": self._generate_highlights(user, original_repos, total_stars, languages),
                "stats": {
                    "username": username,
                    "public_repos": len(original_repos),
                    "followers": user.followers,
                    "following": user.following,
                    "total_stars": total_stars,
                    "total_forks": total_forks,
                    "languages": languages,
                    "recent_activity": len(recent_repos),
                    "account_age_days": (datetime.now() - user.created_at.replace(tzinfo=None)).days
                }
            }
        except GithubException as e:
            if e.status == 404:
                raise Exception(f"GitHub user '{username}' not found")
            elif e.status == 403:
                raise Exception("GitHub API rate limit exceeded. Please add a GitHub token.")
            else:
                raise Exception(f"GitHub API error: {str(e)}")
        except Exception as e:
            raise Exception(f"GitHub analysis failed: {str(e)}")
    
    def _calculate_code_quality(self, repos: List) -> float:
        """Calculate code quality score based on documentation and best practices"""
        if not repos:
            return 0
        
        quality_indicators = 0
        total_checks = 0
        
        for repo in repos[:20]:  # Check top 20 repos
            total_checks += 4
            
            # Has README
            if repo.description or repo.has_wiki:
                quality_indicators += 1
            
            # Has documentation
            if repo.has_wiki or repo.has_pages:
                quality_indicators += 1
            
            # Has issues enabled (shows engagement)
            if repo.has_issues:
                quality_indicators += 1
            
            # Not empty (has commits)
            if repo.size > 0:
                quality_indicators += 1
        
        return min((quality_indicators / total_checks) * 100, 100) if total_checks > 0 else 0
    
    def _calculate_activity(self, user, recent_repos: List, all_repos: List) -> float:
        """Calculate activity score based on recent contributions"""
        if not all_repos:
            return 0
        
        # Recent activity weight
        recent_activity_score = min(len(recent_repos) * 5, 50)
        
        # Total repos weight
        total_repos_score = min(len(all_repos) * 2, 30)
        
        # Contribution consistency (repos with recent pushes)
        consistency_score = (len(recent_repos) / max(len(all_repos), 1)) * 20
        
        return min(recent_activity_score + total_repos_score + consistency_score, 100)
    
    def _calculate_impact(self, stars: int, forks: int, followers: int) -> float:
        """Calculate impact score based on community engagement"""
        # Logarithmic scale for stars (1 star = 1 point, 100 stars = 20 points, 1000 stars = 30 points)
        star_score = min(stars ** 0.5 * 3, 40)
        
        # Fork score
        fork_score = min(forks ** 0.5 * 2, 30)
        
        # Follower score
        follower_score = min(followers ** 0.5 * 2, 30)
        
        return min(star_score + fork_score + follower_score, 100)
    
    def _calculate_diversity(self, languages: Dict) -> float:
        """Calculate diversity score based on language variety"""
        num_languages = len(languages)
        
        # More languages = higher diversity
        diversity_score = min(num_languages * 12, 80)
        
        # Bonus for balanced usage (not just one dominant language)
        if num_languages > 1:
            values = list(languages.values())
            if max(values) / sum(values) < 0.7:  # No single language dominates
                diversity_score += 20
        
        return min(diversity_score, 100)
    
    def _generate_highlights(self, user, repos: List, total_stars: int, languages: Dict) -> List[str]:
        """Generate key highlights from the profile"""
        highlights = []
        
        if total_stars > 100:
            highlights.append(f"Earned {total_stars}+ stars across projects")
        elif total_stars > 10:
            highlights.append(f"{total_stars} stars on repositories")
        
        if user.followers > 100:
            highlights.append(f"{user.followers} followers on GitHub")
        elif user.followers > 20:
            highlights.append(f"{user.followers} followers")
        
        if len(repos) > 50:
            highlights.append(f"Maintains {len(repos)}+ repositories")
        elif len(repos) > 10:
            highlights.append(f"{len(repos)} public repositories")
        
        if len(languages) > 5:
            highlights.append(f"Proficient in {len(languages)}+ programming languages")
            top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
            highlights.append(f"Top languages: {', '.join([lang[0] for lang in top_langs])}")
        
        # Account age
        account_age_years = (datetime.now() - user.created_at.replace(tzinfo=None)).days / 365
        if account_age_years > 5:
            highlights.append(f"{int(account_age_years)}+ years on GitHub")
        
        if not highlights:
            highlights.append("Active GitHub profile")
        
        return highlights[:5]  # Return top 5 highlights
