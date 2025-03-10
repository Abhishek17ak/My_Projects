import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

class ResumeJobMatcher:
    """
    A class for matching resumes with job descriptions and calculating match scores.
    """
    
    def __init__(self):
        """Initialize the ResumeJobMatcher with NLP model."""
        self.nlp = spacy.load("en_core_web_lg")
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Scoring weights
        self.weights = {
            "skills": {
                "technical": 0.25,
                "soft": 0.15,
                "domain": 0.20
            },
            "education": 0.20,
            "experience": 0.20
        }
        
        # Experience scoring parameters
        self.experience_score_params = {
            "exact_match": 1.0,
            "exceed_required": 0.9,
            "close_match": 0.7,  # Within 2 years
            "minimum_match": 0.4  # At least 50% of required
        }

    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate the similarity between two text documents using TF-IDF and cosine similarity.
        
        Args:
            text1: First text document
            text2: Second text document
            
        Returns:
            Similarity score between 0 and 1
        """
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except:
            # Fallback to spaCy similarity if TF-IDF fails (e.g., with very short texts)
            doc1 = self.nlp(text1)
            doc2 = self.nlp(text2)
            return doc1.similarity(doc2)
    
    def calculate_skills_match(self, resume_skills: List[str], job_skills: List[str]) -> Tuple[float, List[str]]:
        """
        Calculate the match score between resume skills and job required skills.
        
        Args:
            resume_skills: List of skills extracted from the resume
            job_skills: List of skills required in the job description
            
        Returns:
            Tuple containing:
                - Match score between 0 and 1
                - List of missing skills
        """
        if not job_skills:
            return 1.0, []  # If no skills are required, it's a perfect match
        
        # Convert to lowercase for case-insensitive matching
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        # Find matching skills
        matching_skills = set(resume_skills_lower).intersection(set(job_skills_lower))
        
        # Calculate match score
        match_score = len(matching_skills) / len(job_skills_lower) if job_skills_lower else 1.0
        
        # Find missing skills
        missing_skills = [skill for skill in job_skills if skill.lower() not in resume_skills_lower]
        
        return match_score, missing_skills
    
    def calculate_education_match(self, resume_education: List[str], job_education: List[str]) -> float:
        """
        Calculate the match score between resume education and job required education.
        
        Args:
            resume_education: List of education entries from the resume
            job_education: List of education requirements from the job description
            
        Returns:
            Match score between 0 and 1
        """
        if not job_education:
            return 1.0  # If no education is required, it's a perfect match
        
        # Combine education entries into a single text
        resume_education_text = " ".join(resume_education)
        job_education_text = " ".join(job_education)
        
        # Calculate similarity
        similarity = self.calculate_text_similarity(resume_education_text, job_education_text)
        
        return similarity
    
    def calculate_experience_match(self, resume_experience: List[str], job_experience: List[str]) -> float:
        """
        Calculate the match score between resume experience and job required experience.
        
        Args:
            resume_experience: List of experience entries from the resume
            job_experience: List of experience requirements from the job description
            
        Returns:
            Match score between 0 and 1
        """
        if not job_experience:
            return 1.0  # If no experience is required, it's a perfect match
        
        # Combine experience entries into a single text
        resume_experience_text = " ".join(resume_experience)
        job_experience_text = " ".join(job_experience)
        
        # Calculate similarity
        similarity = self.calculate_text_similarity(resume_experience_text, job_experience_text)
        
        return similarity
    
    def calculate_skill_score(self, resume_skills: Dict[str, List[str]], job_skills: Dict[str, List[str]]) -> Dict[str, Any]:
        """Calculate detailed skill match scores."""
        skill_scores = {}
        total_weight = 0
        weighted_score = 0
        
        for category in ["technical", "soft", "domain"]:
            if category in job_skills and job_skills[category]:
                resume_category_skills = set(skill.lower() for skill in resume_skills.get(category, []))
                job_category_skills = set(skill.lower() for skill in job_skills[category])
                
                if job_category_skills:
                    matched_skills = resume_category_skills.intersection(job_category_skills)
                    category_score = len(matched_skills) / len(job_category_skills) * 100
                    
                    skill_scores[category] = {
                        "score": category_score,
                        "matched": list(matched_skills),
                        "missing": list(job_category_skills - resume_category_skills),
                        "additional": list(resume_category_skills - job_category_skills)
                    }
                    
                    weight = self.weights["skills"][category]
                    weighted_score += category_score * weight
                    total_weight += weight
        
        if total_weight > 0:
            final_score = weighted_score / total_weight
        else:
            final_score = 0
        
        return {
            "detailed_scores": skill_scores,
            "overall_score": final_score,
            "weight": self.weights["skills"]["technical"] + self.weights["skills"]["soft"] + self.weights["skills"]["domain"]
        }

    def calculate_education_score(self, resume_education: List[Dict[str, Any]], job_education: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed education match score."""
        if not job_education.get("level"):
            return {"score": 100, "weight": self.weights["education"], "details": "No specific education requirements"}
        
        # Get highest education level from resume
        resume_level = max([edu.get("level", 0.0) for edu in resume_education], default=0.0)
        required_level = job_education.get("level", 0.0)
        
        # Calculate base score
        if resume_level >= required_level:
            base_score = 100
        else:
            base_score = (resume_level / required_level) * 100 if required_level > 0 else 0
        
        # Check field match if specified
        field_score = 100
        if job_education.get("fields"):
            resume_fields = " ".join([edu.get("field", "").lower() for edu in resume_education if edu.get("field")])
            job_fields = " ".join([field.lower() for field in job_education["fields"]])
            
            if resume_fields and job_fields:
                # Use TF-IDF and cosine similarity for field matching
                tfidf_matrix = self.vectorizer.fit_transform([resume_fields, job_fields])
                field_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
        
        # Combine scores
        final_score = (base_score * 0.7 + field_score * 0.3)
        
        return {
            "score": final_score,
            "weight": self.weights["education"],
            "details": {
                "resume_level": resume_level,
                "required_level": required_level,
                "field_match_score": field_score
            }
        }

    def calculate_experience_score(self, resume_experience: List[Dict[str, Any]], job_experience: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed experience match score."""
        current_year = datetime.now().year

        # Calculate total years including present positions
        resume_years = 0
        for exp in resume_experience:
            years = exp.get("years", 0.0)
            # Handle "present" or ongoing positions
            if isinstance(exp.get("duration"), str) and any(word in exp["duration"].lower() for word in ["present", "current", "now"]):
                # If it's a current position, calculate years from start year to now
                if "start_year" in exp:
                    years = current_year - exp["start_year"]
                else:
                    # If no start year, use the provided years or default to 0
                    years = exp.get("years", 0.0)
            resume_years += years

        required_years = job_experience.get("required_years", 0.0)
        preferred_years = job_experience.get("preferred_years", 0.0)
        
        if required_years == 0:
            return {"score": 100, "weight": self.weights["experience"], "details": "No specific experience requirements"}
        
        # Calculate base score based on years
        if resume_years >= preferred_years and preferred_years > required_years:
            base_score = 100  # Exceeds preferred experience
        elif resume_years >= required_years:
            if preferred_years > required_years:
                # Scale between required and preferred
                base_score = 80 + (resume_years - required_years) / (preferred_years - required_years) * 20
            else:
                base_score = 100
        elif resume_years >= required_years * 0.75:
            # Close to required experience
            base_score = 70 + (resume_years / required_years) * 30
        else:
            # Below required experience
            base_score = (resume_years / required_years) * 70
        
        # Check for leadership experience if required
        leadership_score = 100
        if job_experience.get("leadership_required"):
            has_leadership = any(
                any(word in exp.get("title", "").lower() for word in ["lead", "manager", "director", "supervisor"])
                for exp in resume_experience
            )
            leadership_score = 100 if has_leadership else 50
        
        # Check for specific requirements
        specific_req_score = 100
        if job_experience.get("specific_requirements"):
            # Combine all experience descriptions
            resume_exp_text = " ".join([
                " ".join(exp.get("responsibilities", []) + exp.get("achievements", []))
                for exp in resume_experience
            ])
            job_req_text = " ".join(job_experience["specific_requirements"])
            
            # Calculate similarity using TF-IDF and cosine similarity
            if resume_exp_text and job_req_text:
                tfidf_matrix = self.vectorizer.fit_transform([resume_exp_text, job_req_text])
                specific_req_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
        
        # Combine scores with weights
        final_score = (base_score * 0.6 + leadership_score * 0.2 + specific_req_score * 0.2)
        
        return {
            "score": final_score,
            "weight": self.weights["experience"],
            "details": {
                "years_match": {
                    "resume_years": resume_years,
                    "required_years": required_years,
                    "preferred_years": preferred_years,
                    "score": base_score
                },
                "leadership_match": {
                    "required": job_experience.get("leadership_required", False),
                    "score": leadership_score
                },
                "specific_requirements_match": {
                    "score": specific_req_score
                }
            }
        }

    def calculate_match_score(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate the overall match score between a resume and job description."""
        # Calculate skill scores
        skill_scores = self.calculate_skill_score(resume_data["skills"], job_data["skills"])
        
        # Calculate education score
        education_score = self.calculate_education_score(resume_data["education"], job_data["education"])
        
        # Calculate experience score
        experience_score = self.calculate_experience_score(resume_data["experience"], job_data["experience"])
        
        # Calculate overall weighted score
        total_score = (
            skill_scores["overall_score"] * skill_scores["weight"] +
            education_score["score"] * education_score["weight"] +
            experience_score["score"] * experience_score["weight"]
        )
        
        # Compile missing skills
        missing_skills = {}
        for category, details in skill_scores["detailed_scores"].items():
            if details["missing"]:
                missing_skills[category] = details["missing"]
        
        # Get improvement suggestions
        improvement_suggestions = self.get_resume_improvements({
            "skill_scores": skill_scores,
            "education_score": education_score,
            "experience_score": experience_score,
            "missing_skills": missing_skills
        }, job_data)
        
        return {
            "overall_score": total_score,
            "component_scores": {
                "skills": skill_scores,
                "education": education_score,
                "experience": experience_score
            },
            "missing_skills": missing_skills,
            "improvement_suggestions": improvement_suggestions
        }

    def get_resume_improvements(self, match_result: Dict[str, Any], job_data: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions based on match results."""
        suggestions = []
        
        # Skills improvements
        skill_scores = match_result["skill_scores"]
        for category, details in skill_scores["detailed_scores"].items():
            if details["score"] < 80:
                missing = details["missing"]
                if missing:
                    suggestions.append(
                        f"Consider acquiring or highlighting these {category} skills: {', '.join(missing)}"
                    )
        
        # Education improvements
        edu_score = match_result["education_score"]
        if edu_score["score"] < 80:
            if job_data["education"].get("required_degree"):
                suggestions.append(
                    f"Consider pursuing {job_data['education']['required_degree']} degree"
                )
            if job_data["education"].get("fields"):
                suggestions.append(
                    f"Consider education in: {', '.join(job_data['education']['fields'])}"
                )
        
        # Experience improvements
        exp_score = match_result["experience_score"]
        if exp_score["score"] < 80:
            years_match = exp_score["details"]["years_match"]
            if years_match["resume_years"] < years_match["required_years"]:
                suggestions.append(
                    f"Gain more experience - currently {years_match['resume_years']:.1f} years vs required {years_match['required_years']:.1f} years"
                )
        
        return suggestions 