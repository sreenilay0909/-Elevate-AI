import os
import re
from typing import Dict, Any, List
from PyPDF2 import PdfReader
from PIL import Image
import google.generativeai as genai
from io import BytesIO

class ResumeService:
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # ATS keywords by category
        self.ats_keywords = {
            "technical_skills": [
                "python", "javascript", "java", "c++", "react", "node.js", "angular", "vue",
                "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git",
                "sql", "mongodb", "postgresql", "mysql", "redis",
                "machine learning", "ai", "data science", "tensorflow", "pytorch"
            ],
            "soft_skills": [
                "leadership", "communication", "teamwork", "problem solving",
                "analytical", "creative", "adaptable", "organized"
            ],
            "action_verbs": [
                "developed", "implemented", "designed", "created", "built", "managed",
                "led", "improved", "optimized", "achieved", "delivered", "collaborated"
            ],
            "certifications": [
                "aws certified", "azure certified", "google cloud", "pmp", "scrum master",
                "cissp", "comptia", "oracle certified"
            ]
        }
    
    async def analyze_resume_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Analyze resume from PDF or image file"""
        try:
            # Determine file type
            file_ext = filename.lower().split('.')[-1]
            
            if file_ext == 'pdf':
                text = self._extract_text_from_pdf(file_content)
            elif file_ext in ['jpg', 'jpeg', 'png', 'webp']:
                text = await self._extract_text_from_image(file_content, file_ext)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            if not text or len(text.strip()) < 50:
                raise ValueError("Could not extract sufficient text from resume. Please ensure the file is readable.")
            
            # Perform comprehensive analysis
            resume_analysis = await self._analyze_resume_content(text)
            ats_score = self._calculate_ats_score(text)
            
            return {
                "name": "Resume",
                "score": resume_analysis.get("overall_score", 0),
                "total": 100.0,
                "metrics": [
                    {"name": "Content Quality", "value": resume_analysis.get("content_quality", 0)},
                    {"name": "ATS Compatibility", "value": ats_score.get("total_score", 0)},
                    {"name": "Skills Match", "value": resume_analysis.get("skills_score", 0)},
                    {"name": "Experience", "value": resume_analysis.get("experience_score", 0)}
                ],
                "highlights": resume_analysis.get("highlights", []),
                "stats": {
                    "extracted_text_length": len(text),
                    "skills_found": resume_analysis.get("skills", []),
                    "experience_years": resume_analysis.get("experience_years", 0),
                    "education": resume_analysis.get("education", []),
                    "ats_analysis": ats_score
                }
            }
        except Exception as e:
            raise Exception(f"Resume analysis failed: {str(e)}")
    
    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = BytesIO(file_content)
            reader = PdfReader(pdf_file)
            
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")
    
    async def _extract_text_from_image(self, file_content: bytes, file_ext: str) -> str:
        """Extract text from image using Gemini Vision"""
        try:
            # Use Gemini Vision to extract text from image
            image_data = BytesIO(file_content)
            image = Image.open(image_data)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Use Gemini to extract text
            prompt = """
            Extract ALL text from this resume image. 
            Preserve the structure and formatting as much as possible.
            Include:
            - Name and contact information
            - Work experience with dates
            - Education details
            - Skills and technologies
            - Projects and achievements
            - Certifications
            
            Return the extracted text in a clean, readable format.
            """
            
            response = self.model.generate_content([prompt, image])
            return response.text.strip()
            
        except Exception as e:
            raise Exception(f"Image text extraction failed: {str(e)}")
    
    async def _analyze_resume_content(self, text: str) -> Dict[str, Any]:
        """Use Gemini AI to analyze resume content"""
        prompt = f"""
        Analyze this resume and provide a comprehensive evaluation in JSON format.
        
        Resume Text:
        {text}
        
        Provide analysis with these fields:
        {{
            "overall_score": <number 0-100>,
            "content_quality": <number 0-100>,
            "skills_score": <number 0-100>,
            "experience_score": <number 0-100>,
            "skills": [<list of technical skills found>],
            "experience_years": <estimated years of experience>,
            "education": [<list of degrees/certifications>],
            "highlights": [<3-5 key strengths>],
            "improvements": [<3-5 suggestions for improvement>]
        }}
        
        Scoring criteria:
        - Content Quality: Clarity, structure, grammar, formatting
        - Skills Score: Relevance and breadth of technical skills
        - Experience Score: Years of experience, impact, achievements
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            import json
            analysis = json.loads(response_text)
            return analysis
            
        except Exception as e:
            # Fallback analysis
            return self._fallback_analysis(text)
    
    def _calculate_ats_score(self, text: str) -> Dict[str, Any]:
        """Calculate ATS (Applicant Tracking System) compatibility score"""
        text_lower = text.lower()
        
        # Check for ATS-friendly elements
        scores = {
            "keyword_optimization": 0,
            "formatting": 0,
            "contact_info": 0,
            "section_headers": 0,
            "action_verbs": 0
        }
        
        # 1. Keyword Optimization (40 points)
        technical_skills_found = sum(1 for skill in self.ats_keywords["technical_skills"] if skill in text_lower)
        soft_skills_found = sum(1 for skill in self.ats_keywords["soft_skills"] if skill in text_lower)
        scores["keyword_optimization"] = min(
            (technical_skills_found * 3 + soft_skills_found * 2) / 2, 
            40
        )
        
        # 2. Formatting (20 points)
        # Check for clean structure
        has_bullets = bool(re.search(r'[•\-\*]', text))
        has_dates = bool(re.search(r'\d{4}', text))
        has_sections = bool(re.search(r'(experience|education|skills|projects)', text_lower))
        scores["formatting"] = (has_bullets * 7 + has_dates * 7 + has_sections * 6)
        
        # 3. Contact Information (15 points)
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        has_phone = bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text))
        has_linkedin = 'linkedin' in text_lower
        scores["contact_info"] = (has_email * 6 + has_phone * 5 + has_linkedin * 4)
        
        # 4. Section Headers (15 points)
        standard_sections = ['experience', 'education', 'skills', 'summary', 'projects']
        sections_found = sum(1 for section in standard_sections if section in text_lower)
        scores["section_headers"] = min(sections_found * 3, 15)
        
        # 5. Action Verbs (10 points)
        action_verbs_found = sum(1 for verb in self.ats_keywords["action_verbs"] if verb in text_lower)
        scores["action_verbs"] = min(action_verbs_found * 2, 10)
        
        total_score = sum(scores.values())
        
        # Generate recommendations
        recommendations = []
        if scores["keyword_optimization"] < 20:
            recommendations.append("Add more relevant technical skills and keywords")
        if scores["formatting"] < 15:
            recommendations.append("Improve formatting with bullet points and clear sections")
        if scores["contact_info"] < 10:
            recommendations.append("Ensure all contact information is present (email, phone, LinkedIn)")
        if scores["section_headers"] < 10:
            recommendations.append("Use standard section headers (Experience, Education, Skills)")
        if scores["action_verbs"] < 5:
            recommendations.append("Use more action verbs to describe achievements")
        
        # ATS compatibility rating
        if total_score >= 80:
            rating = "Excellent"
            message = "Your resume is highly ATS-compatible"
        elif total_score >= 60:
            rating = "Good"
            message = "Your resume is ATS-friendly with room for improvement"
        elif total_score >= 40:
            rating = "Fair"
            message = "Your resume needs optimization for ATS systems"
        else:
            rating = "Poor"
            message = "Your resume may not pass ATS screening"
        
        return {
            "total_score": round(total_score, 2),
            "rating": rating,
            "message": message,
            "breakdown": scores,
            "recommendations": recommendations,
            "keywords_found": {
                "technical_skills": technical_skills_found,
                "soft_skills": soft_skills_found,
                "action_verbs": action_verbs_found
            }
        }
    
    def _fallback_analysis(self, text: str) -> Dict[str, Any]:
        """Fallback analysis if AI fails"""
        text_lower = text.lower()
        
        # Extract skills
        skills = [skill for skill in self.ats_keywords["technical_skills"] if skill in text_lower]
        
        # Estimate experience
        years_matches = re.findall(r'(\d+)\+?\s*years?', text_lower)
        experience_years = max([int(y) for y in years_matches], default=0)
        
        # Find education
        education = []
        edu_keywords = ["bachelor", "master", "phd", "b.tech", "m.tech", "mba", "degree"]
        for keyword in edu_keywords:
            if keyword in text_lower:
                education.append(keyword.title())
        
        return {
            "overall_score": 65,
            "content_quality": 70,
            "skills_score": min(len(skills) * 5, 100),
            "experience_score": min(experience_years * 10, 100),
            "skills": skills[:10],
            "experience_years": experience_years,
            "education": list(set(education)),
            "highlights": [
                f"Found {len(skills)} technical skills",
                f"Approximately {experience_years} years of experience",
                "Resume structure detected"
            ],
            "improvements": [
                "Add more quantifiable achievements",
                "Include specific project outcomes",
                "Optimize for ATS keywords"
            ]
        }
