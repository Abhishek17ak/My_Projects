import spacy
import re
from typing import Dict, List, Any, Optional
from transformers import pipeline

class JobParser:
    """
    A class for parsing and extracting information from job descriptions.
    """
    
    def __init__(self):
        """Initialize the JobParser with NLP models."""
        self.nlp = spacy.load("en_core_web_lg")
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        
        # Enhanced skill patterns with categories
        self.skill_patterns = {
            "technical": [
                "python", "java", "javascript", "typescript", "c\\+\\+", "ruby", "php", "swift",
                "kotlin", "rust", "golang", "sql", "nosql", "mongodb", "postgresql", "mysql",
                "oracle", "redis", "elasticsearch", "aws", "azure", "gcp", "docker", "kubernetes",
                "jenkins", "git", "terraform", "ansible", "react", "angular", "vue", "node.js",
                "django", "flask", "spring", "tensorflow", "pytorch", "scikit-learn", "pandas",
                "numpy", "hadoop", "spark", "kafka", "graphql", "rest", "soap", "microservices"
            ],
            "soft": [
                "leadership", "communication", "teamwork", "problem solving", "critical thinking",
                "time management", "project management", "agile", "scrum", "stakeholder management",
                "presentation", "negotiation", "conflict resolution", "mentoring", "coaching"
            ],
            "domain": [
                "machine learning", "artificial intelligence", "data science", "cloud computing",
                "devops", "cybersecurity", "blockchain", "iot", "web development", "mobile development",
                "database administration", "system architecture", "ui/ux design", "business intelligence"
            ]
        }
        
        # Education degree levels and their weights
        self.education_levels = {
            "phd": 1.0,
            "doctorate": 1.0,
            "master": 0.8,
            "mba": 0.8,
            "bachelor": 0.6,
            "associate": 0.4,
            "certification": 0.3
        }
        
        # Experience level patterns
        self.experience_patterns = [
            (r"(\d+)\+?\s*(?:years?|yrs?)", lambda x: int(x)),
            (r"(\d+)-(\d+)\s*(?:years?|yrs?)", lambda x, y: (int(x) + int(y)) / 2),
            (r"(?:minimum|min\.?|at least)\s*(\d+)\s*(?:years?|yrs?)", lambda x: int(x))
        ]
        
        # Salary patterns
        self.salary_patterns = [
            # Annual salary ranges
            (r"\$(\d{2,3}(?:,\d{3})*)-\$?(\d{2,3}(?:,\d{3})*)\s*(?:per year|yearly|/year|annually|k/year|k per year)", 
             lambda x, y: {"min": float(x.replace(",", "")), "max": float(y.replace(",", "")), "period": "annual"}),
            (r"\$(\d{2,3}(?:,\d{3})*k?)(?:\s*-\s*\$?(\d{2,3}(?:,\d{3})*k?))?\s*(?:per year|yearly|/year|annually)", 
             lambda x, y: {"min": float(x.replace(",", "").replace("k", "000")), 
                          "max": float((y or x).replace(",", "").replace("k", "000")), 
                          "period": "annual"}),
            # Hourly rates
            (r"\$(\d{2,3}(?:\.\d{2})?)-\$?(\d{2,3}(?:\.\d{2})?)\s*(?:per hour|hourly|/hour|/hr)", 
             lambda x, y: {"min": float(x), "max": float(y), "period": "hourly"}),
            (r"\$(\d{2,3}(?:\.\d{2})?)\s*(?:per hour|hourly|/hour|/hr)", 
             lambda x: {"min": float(x), "max": float(x), "period": "hourly"})
        ]
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract required skills with categories using advanced NLP."""
        skills = {category: [] for category in self.skill_patterns.keys()}
        doc = self.nlp(text.lower())
        
        # Extract skills using pattern matching and NLP
        for category, patterns in self.skill_patterns.items():
            for skill in patterns:
                if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
                    # Verify skill using word embeddings and context
                    skill_doc = self.nlp(skill)
                    context_window = 10
                    for token in doc:
                        if token.text.lower() == skill.lower():
                            context = doc[max(0, token.i - context_window):min(len(doc), token.i + context_window)]
                            if any(context.similarity(skill_doc) > 0.7 for context in [self.nlp(sent.text) for sent in context.sents]):
                                skills[category].append(skill)
                                break
        
        return {k: list(set(v)) for k, v in skills.items()}
    
    def extract_education(self, text: str) -> Dict[str, Any]:
        """Extract education requirements using NLP."""
        doc = self.nlp(text)
        education_info = {
            "required_degree": None,
            "preferred_degree": None,
            "level": 0.0,
            "fields": []
        }
        
        # Find education-related sentences
        edu_sentences = []
        for sent in doc.sents:
            if any(edu_word in sent.text.lower() for edu_word in ["degree", "education", "bachelor", "master", "phd"]):
                edu_sentences.append(sent.text)
        
        # Process education sentences
        for sent in edu_sentences:
            sent_lower = sent.lower()
            
            # Determine if required or preferred
            is_required = any(word in sent_lower for word in ["required", "must have", "minimum"])
            is_preferred = any(word in sent_lower for word in ["preferred", "desired", "ideal"])
            
            # Extract degree level
            for degree, weight in self.education_levels.items():
                if degree in sent_lower:
                    if is_required:
                        education_info["required_degree"] = degree
                        education_info["level"] = max(education_info["level"], weight)
                    elif is_preferred:
                        education_info["preferred_degree"] = degree
                        if not education_info["required_degree"]:  # Only update level if no required degree
                            education_info["level"] = max(education_info["level"], weight * 0.8)  # Preferred degrees weighted less
            
            # Extract fields of study
            fields_doc = self.nlp(sent)
            for ent in fields_doc.ents:
                if ent.label_ == "ORG" and any(field in ent.text.lower() for field in 
                    ["computer science", "engineering", "mathematics", "statistics", "physics",
                     "business", "economics", "finance", "accounting", "marketing"]):
                    education_info["fields"].append(ent.text)
        
        education_info["fields"] = list(set(education_info["fields"]))
        return education_info
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience requirements using advanced NLP."""
        doc = self.nlp(text)
        experience_info = {
            "total_years": 0.0,
            "required_years": 0.0,
            "preferred_years": 0.0,
            "specific_requirements": [],
            "leadership_required": False,
            "remote_work": False
        }
        
        # Process each sentence
        for sent in doc.sents:
            sent_text = sent.text.lower()
            
            # Extract years of experience
            for pattern, converter in self.experience_patterns:
                matches = re.findall(pattern, sent_text)
                if matches:
                    years = converter(*matches[0] if isinstance(matches[0], tuple) else matches)
                    if "required" in sent_text or "must have" in sent_text:
                        experience_info["required_years"] = max(experience_info["required_years"], years)
                    elif "preferred" in sent_text or "desired" in sent_text:
                        experience_info["preferred_years"] = max(experience_info["preferred_years"], years)
                    experience_info["total_years"] = max(experience_info["total_years"], years)
            
            # Check for leadership requirements
            if any(word in sent_text for word in ["lead", "manage", "supervise", "direct"]):
                experience_info["leadership_required"] = True
            
            # Check for remote work
            if any(word in sent_text for word in ["remote", "work from home", "telecommute", "virtual"]):
                experience_info["remote_work"] = True
            
            # Extract specific requirements
            if any(word in sent_text for word in ["experience with", "experience in", "proficiency in"]):
                experience_info["specific_requirements"].append(sent.text.strip())
        
        return experience_info
    
    def extract_salary(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract salary information using regex patterns."""
        text = text.replace('\n', ' ')
        
        for pattern, converter in self.salary_patterns:
            matches = re.search(pattern, text)
            if matches:
                try:
                    salary_info = converter(*matches.groups())
                    # Convert hourly to annual if needed
                    if salary_info["period"] == "hourly":
                        annual_min = salary_info["min"] * 40 * 52  # 40 hours/week, 52 weeks/year
                        annual_max = salary_info["max"] * 40 * 52
                        salary_info.update({
                            "min": annual_min,
                            "max": annual_max,
                            "period": "annual",
                            "original": {
                                "min": salary_info["min"],
                                "max": salary_info["max"],
                                "period": "hourly"
                            }
                        })
                    return salary_info
                except Exception:
                    continue
        return None
    
    def extract_company_info(self, text: str) -> Dict[str, Any]:
        """Extract company information using NER and pattern matching."""
        doc = self.nlp(text)
        company_info = {
            "name": None,
            "industry": None,
            "location": None,
            "company_size": None,
            "work_model": "unspecified"  # onsite, remote, hybrid, or unspecified
        }
        
        # Extract company name and location using NER
        for ent in doc.ents:
            if ent.label_ == "ORG" and not company_info["name"]:
                company_info["name"] = ent.text
            elif ent.label_ in ["GPE", "LOC"] and not company_info["location"]:
                company_info["location"] = ent.text
        
        # Extract work model
        text_lower = text.lower()
        if "remote" in text_lower or "work from home" in text_lower:
            company_info["work_model"] = "remote"
        elif "hybrid" in text_lower:
            company_info["work_model"] = "hybrid"
        elif "onsite" in text_lower or "in office" in text_lower:
            company_info["work_model"] = "onsite"
        
        # Extract company size
        size_patterns = [
            (r"(\d+(?:,\d+)?)\s*(?:-|to)\s*(\d+(?:,\d+)?)\s*employees", 
             lambda x, y: f"{x}-{y} employees"),
            (r"(\d+(?:,\d+)?)\+\s*employees", 
             lambda x: f"{x}+ employees")
        ]
        
        for pattern, converter in size_patterns:
            match = re.search(pattern, text)
            if match:
                company_info["company_size"] = converter(*match.groups())
                break
        
        return company_info
    
    def parse_job_description(self, text: str) -> Dict[str, Any]:
        """Parse job description and extract all relevant information."""
        # Extract all components
        skills = self.extract_skills(text)
        education = self.extract_education(text)
        experience = self.extract_experience(text)
        salary = self.extract_salary(text)
        company = self.extract_company_info(text)
        
        # Create job requirements summary
        requirements = {
            "education": education,
            "experience": experience,
            "skills": skills,
            "salary": salary,
            "company": company,
            "raw_text": text
        }
        
        return requirements 