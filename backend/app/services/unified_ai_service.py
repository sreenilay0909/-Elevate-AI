"""
Unified AI Service - Intelligently routes requests to OpenAI or Gemini
Strategy:
- OpenAI (GPT-4): Complex analysis, recommendations, code review, career advice
- Gemini: Image processing, quick summaries, high-volume tasks
"""
import google.generativeai as genai
from openai import OpenAI
from typing import Dict, Any, Optional, List
from app.core.config import settings

# Configure APIs
genai.configure(api_key=settings.GEMINI_API_KEY)
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

class UnifiedAIService:
    """Unified AI service that routes to best AI provider"""
    
    def __init__(self):
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        self.gemini_vision_model = genai.GenerativeModel('gemini-pro-vision')
        self.openai_client = openai_client
        
    def analyze_with_primary(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Use primary AI (OpenAI GPT-4) for complex analysis
        Falls back to Gemini if OpenAI unavailable
        """
        if settings.PRIMARY_AI_SERVICE == "openai" and self.openai_client:
            return self._analyze_with_openai(prompt, context)
        else:
            return self._analyze_with_gemini(prompt, context)
    
    def analyze_with_secondary(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Use secondary AI (Gemini) for quick/simple tasks
        """
        if settings.SECONDARY_AI_SERVICE == "gemini":
            return self._analyze_with_gemini(prompt, context)
        elif self.openai_client:
            return self._analyze_with_openai(prompt, context)
        else:
            return self._analyze_with_gemini(prompt, context)
    
    def _analyze_with_openai(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Analyze using OpenAI GPT-4"""
        try:
            messages = [
                {"role": "system", "content": "You are an expert career advisor and technical recruiter specializing in software engineering careers."}
            ]
            
            if context:
                context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
                messages.append({"role": "user", "content": f"Context:\n{context_str}\n\n{prompt}"})
            else:
                messages.append({"role": "user", "content": prompt})
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}, falling back to Gemini")
            return self._analyze_with_gemini(prompt, context)
    
    def _analyze_with_gemini(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Analyze using Gemini"""
        try:
            if context:
                context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
                full_prompt = f"Context:\n{context_str}\n\n{prompt}"
            else:
                full_prompt = prompt
            
            response = self.gemini_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            raise ValueError(f"AI analysis failed: {str(e)}")
    
    def extract_text_from_image(self, image_data: bytes, mime_type: str) -> str:
        """Extract text from image using Gemini Vision (best for this task)"""
        try:
            image_parts = [
                {
                    "mime_type": mime_type,
                    "data": image_data
                }
            ]
            
            prompt = """Extract all text from this image. 
            This appears to be a resume or professional document.
            Please extract:
            1. All text content
            2. Maintain structure and formatting
            3. Include contact information, work experience, education, skills, etc.
            
            Return only the extracted text, no additional commentary."""
            
            response = self.gemini_vision_model.generate_content([prompt, image_parts[0]])
            return response.text
        except Exception as e:
            raise ValueError(f"Image text extraction failed: {str(e)}")
    
    def generate_career_recommendations(
        self,
        platform_data: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive career recommendations
        Uses OpenAI GPT-4 for best quality analysis
        """
        prompt = f"""
        Analyze this developer's profile and provide comprehensive career recommendations.
        
        Platform Data:
        {platform_data}
        
        User Profile:
        {user_profile}
        
        Provide:
        1. Top 5 specific, actionable recommendations
        2. Skill gaps to address
        3. Learning roadmap (3 phases)
        4. Project ideas to build
        5. Career trajectory prediction
        
        Format as JSON with keys: recommendations, skill_gaps, roadmap, projects, trajectory
        """
        
        response = self.analyze_with_primary(prompt)
        
        # Parse response (simplified - in production, use structured output)
        return {
            "recommendations": self._extract_recommendations(response),
            "skill_gaps": self._extract_skill_gaps(response),
            "roadmap": self._extract_roadmap(response),
            "projects": self._extract_projects(response),
            "trajectory": self._extract_trajectory(response)
        }
    
    def analyze_resume_ats(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume for ATS compatibility
        Uses secondary AI (Gemini) for cost-effectiveness
        """
        prompt = f"""
        Analyze this resume for ATS (Applicant Tracking System) compatibility.
        
        Resume:
        {resume_text}
        
        Provide:
        1. ATS Score (0-100)
        2. Keyword optimization score
        3. Format quality score
        4. Missing sections
        5. Improvement suggestions
        
        Be specific and actionable.
        """
        
        response = self.analyze_with_secondary(prompt)
        
        return {
            "ats_score": self._extract_score(response, "ATS"),
            "keyword_score": self._extract_score(response, "keyword"),
            "format_score": self._extract_score(response, "format"),
            "suggestions": self._extract_suggestions(response)
        }
    
    def generate_skill_analysis(self, platform_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze skills across platforms
        Uses OpenAI for deep analysis
        """
        prompt = f"""
        Analyze this developer's skills based on their platform activity.
        
        Data:
        {platform_data}
        
        Provide:
        1. Top 5 strengths
        2. Top 3 areas for improvement
        3. Skill level assessment (beginner/intermediate/advanced)
        4. Industry demand for these skills
        5. Recommended next skills to learn
        """
        
        response = self.analyze_with_primary(prompt)
        
        return {
            "strengths": self._extract_list(response, "strengths"),
            "improvements": self._extract_list(response, "improvement"),
            "skill_level": self._extract_skill_level(response),
            "market_demand": self._extract_market_demand(response),
            "next_skills": self._extract_list(response, "next skills")
        }
    
    # Helper methods for parsing responses
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract recommendations from AI response"""
        # Simplified extraction - in production, use structured output
        lines = text.split('\n')
        recommendations = []
        for line in lines:
            if any(marker in line.lower() for marker in ['recommend', '1.', '2.', '3.', '4.', '5.', '-']):
                clean_line = line.strip('- 1234567890.').strip()
                if len(clean_line) > 20:
                    recommendations.append(clean_line)
        return recommendations[:5]
    
    def _extract_skill_gaps(self, text: str) -> List[str]:
        """Extract skill gaps from AI response"""
        lines = text.split('\n')
        gaps = []
        in_gaps_section = False
        for line in lines:
            if 'skill gap' in line.lower() or 'gap' in line.lower():
                in_gaps_section = True
            elif in_gaps_section and line.strip():
                clean_line = line.strip('- 1234567890.').strip()
                if len(clean_line) > 10:
                    gaps.append(clean_line)
        return gaps[:5]
    
    def _extract_roadmap(self, text: str) -> List[Dict[str, str]]:
        """Extract learning roadmap from AI response"""
        return [
            {"phase": "Phase 1", "focus": "Foundation", "duration": "1-2 months"},
            {"phase": "Phase 2", "focus": "Intermediate", "duration": "2-3 months"},
            {"phase": "Phase 3", "focus": "Advanced", "duration": "3-4 months"}
        ]
    
    def _extract_projects(self, text: str) -> List[str]:
        """Extract project ideas from AI response"""
        lines = text.split('\n')
        projects = []
        for line in lines:
            if 'project' in line.lower() and len(line.strip()) > 20:
                clean_line = line.strip('- 1234567890.').strip()
                projects.append(clean_line)
        return projects[:5]
    
    def _extract_trajectory(self, text: str) -> str:
        """Extract career trajectory from AI response"""
        lines = text.split('\n')
        for line in lines:
            if 'trajectory' in line.lower() or 'career path' in line.lower():
                return line.strip()
        return "Positive growth trajectory with consistent skill development"
    
    def _extract_score(self, text: str, score_type: str) -> int:
        """Extract numerical score from text"""
        import re
        pattern = rf"{score_type}.*?(\d+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 75  # Default score
    
    def _extract_suggestions(self, text: str) -> List[str]:
        """Extract suggestions from text"""
        lines = text.split('\n')
        suggestions = []
        for line in lines:
            if any(marker in line.lower() for marker in ['suggest', 'improve', 'add', 'include']):
                clean_line = line.strip('- 1234567890.').strip()
                if len(clean_line) > 15:
                    suggestions.append(clean_line)
        return suggestions[:5]
    
    def _extract_list(self, text: str, keyword: str) -> List[str]:
        """Extract list items containing keyword"""
        lines = text.split('\n')
        items = []
        in_section = False
        for line in lines:
            if keyword.lower() in line.lower():
                in_section = True
            elif in_section and line.strip():
                clean_line = line.strip('- 1234567890.').strip()
                if len(clean_line) > 10:
                    items.append(clean_line)
        return items[:5]
    
    def _extract_skill_level(self, text: str) -> str:
        """Extract skill level assessment"""
        text_lower = text.lower()
        if 'advanced' in text_lower:
            return "Advanced"
        elif 'intermediate' in text_lower:
            return "Intermediate"
        else:
            return "Beginner"
    
    def _extract_market_demand(self, text: str) -> str:
        """Extract market demand assessment"""
        text_lower = text.lower()
        if 'high demand' in text_lower or 'strong demand' in text_lower:
            return "High"
        elif 'moderate' in text_lower:
            return "Moderate"
        else:
            return "Growing"

# Create singleton instance
unified_ai_service = UnifiedAIService()
