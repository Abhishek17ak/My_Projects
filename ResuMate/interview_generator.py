import random
from typing import Dict, List, Any

class InterviewGenerator:
    """
    A class for generating interview questions based on resume and job description.
    """
    
    def __init__(self):
        """Initialize the InterviewGenerator with question templates."""
        # General interview question templates
        self.general_questions = [
            "Tell me about yourself.",
            "Why are you interested in this position?",
            "What are your strengths and weaknesses?",
            "Where do you see yourself in 5 years?",
            "Why should we hire you?",
            "Tell me about a challenge you faced and how you overcame it.",
            "How do you handle stress and pressure?",
            "What is your greatest professional achievement?",
            "Describe your ideal work environment.",
            "How would your colleagues describe you?"
        ]
        
        # Skill-based question templates
        self.skill_question_templates = [
            "Can you describe your experience with {skill}?",
            "How have you used {skill} in your previous roles?",
            "What projects have you completed using {skill}?",
            "Rate your proficiency in {skill} on a scale of 1-10 and explain why.",
            "How do you stay updated with the latest developments in {skill}?",
            "Can you give an example of a problem you solved using {skill}?",
            "What aspects of {skill} are you most comfortable with?",
            "How would you explain {skill} to someone with no technical background?"
        ]
        
        # Experience-based question templates
        self.experience_question_templates = [
            "Tell me more about your role at {company}.",
            "What were your main responsibilities as a {position}?",
            "What achievements are you most proud of from your time at {company}?",
            "How did your work at {company} prepare you for this role?",
            "What challenges did you face in your role as {position} and how did you overcome them?",
            "Can you describe a project you led at {company}?",
            "How did you collaborate with team members in your role at {company}?"
        ]
        
        # Education-based question templates
        self.education_question_templates = [
            "How has your education in {field} prepared you for this role?",
            "What courses or projects during your education are most relevant to this position?",
            "Why did you choose to study {field}?",
            "How do you apply what you learned in {field} to your professional work?",
            "What additional training or education have you pursued since completing your degree in {field}?"
        ]
        
        # Missing skill question templates
        self.missing_skill_question_templates = [
            "We noticed {skill} wasn't mentioned in your resume. Do you have any experience with it?",
            "This role requires {skill}. How would you plan to develop this skill if hired?",
            "Are you familiar with {skill}, even though it's not listed on your resume?",
            "How quickly do you think you could become proficient in {skill}?",
            "Have you worked with technologies similar to {skill} that might help you learn it quickly?"
        ]
    
    def generate_general_questions(self, num_questions: int = 3) -> List[str]:
        """
        Generate general interview questions.
        
        Args:
            num_questions: Number of questions to generate
            
        Returns:
            List of general interview questions
        """
        return random.sample(self.general_questions, min(num_questions, len(self.general_questions)))
    
    def generate_skill_questions(self, skills: List[str], num_questions: int = 3) -> List[str]:
        """
        Generate skill-based interview questions.
        
        Args:
            skills: List of skills to generate questions about
            num_questions: Maximum number of questions to generate
            
        Returns:
            List of skill-based interview questions
        """
        questions = []
        
        # Select a random subset of skills if there are more than num_questions
        selected_skills = random.sample(skills, min(num_questions, len(skills)))
        
        for skill in selected_skills:
            # Select a random question template
            template = random.choice(self.skill_question_templates)
            # Fill in the template with the skill
            question = template.format(skill=skill)
            questions.append(question)
        
        return questions
    
    def generate_missing_skill_questions(self, missing_skills: List[str], num_questions: int = 2) -> List[str]:
        """
        Generate questions about skills missing from the resume but required for the job.
        
        Args:
            missing_skills: List of skills missing from the resume
            num_questions: Maximum number of questions to generate
            
        Returns:
            List of questions about missing skills
        """
        questions = []
        
        # Select a random subset of missing skills if there are more than num_questions
        selected_skills = random.sample(missing_skills, min(num_questions, len(missing_skills))) if missing_skills else []
        
        for skill in selected_skills:
            # Select a random question template
            template = random.choice(self.missing_skill_question_templates)
            # Fill in the template with the skill
            question = template.format(skill=skill)
            questions.append(question)
        
        return questions
    
    def generate_experience_questions(self, resume_data: Dict[str, Any], num_questions: int = 2) -> List[str]:
        """
        Generate experience-based interview questions.
        
        Args:
            resume_data: Dictionary containing parsed resume information
            num_questions: Maximum number of questions to generate
            
        Returns:
            List of experience-based interview questions
        """
        questions = []
        
        # Extract company and position information from experience
        companies = []
        positions = []
        
        for exp in resume_data.get("experience", []):
            # Try to extract company and position information using simple heuristics
            words = exp.split()
            for i, word in enumerate(words):
                if word.lower() in ["at", "for", "with"] and i < len(words) - 1:
                    companies.append(words[i+1].strip(",."))
                if word.lower() in ["as", "position", "role", "title"] and i < len(words) - 1:
                    positions.append(words[i+1].strip(",."))
        
        # Generate questions based on companies
        for company in companies[:num_questions//2]:
            if company:
                template = random.choice(self.experience_question_templates)
                if "{company}" in template and "{position}" not in template:
                    question = template.format(company=company)
                    questions.append(question)
        
        # Generate questions based on positions
        for position in positions[:num_questions//2]:
            if position:
                template = random.choice(self.experience_question_templates)
                if "{position}" in template and "{company}" not in template:
                    question = template.format(position=position)
                    questions.append(question)
        
        return questions
    
    def generate_education_questions(self, resume_data: Dict[str, Any], num_questions: int = 1) -> List[str]:
        """
        Generate education-based interview questions.
        
        Args:
            resume_data: Dictionary containing parsed resume information
            num_questions: Maximum number of questions to generate
            
        Returns:
            List of education-based interview questions
        """
        questions = []
        
        # Extract field of study information from education
        fields = []
        
        for edu in resume_data.get("education", []):
            # Try to extract field of study using simple heuristics
            words = edu.split()
            for i, word in enumerate(words):
                if word.lower() in ["in", "of", "degree"] and i < len(words) - 1:
                    fields.append(words[i+1].strip(",."))
        
        # Generate questions based on fields of study
        for field in fields[:num_questions]:
            if field:
                template = random.choice(self.education_question_templates)
                question = template.format(field=field)
                questions.append(question)
        
        return questions
    
    def generate_interview_questions(self, resume_data: Dict[str, Any], job_data: Dict[str, Any], 
                                    match_result: Dict[str, Any], num_questions: int = 10) -> List[str]:
        """
        Generate a comprehensive set of interview questions based on resume, job description, and match results.
        
        Args:
            resume_data: Dictionary containing parsed resume information
            job_data: Dictionary containing parsed job information
            match_result: Dictionary containing match scores and missing skills
            num_questions: Total number of questions to generate
            
        Returns:
            List of interview questions
        """
        all_questions = []
        
        # Allocate questions by category
        general_count = max(1, num_questions // 5)
        skill_count = max(1, num_questions // 3)
        missing_skill_count = min(2, len(match_result.get("missing_skills", [])))
        experience_count = max(1, num_questions // 5)
        education_count = max(1, num_questions // 10)
        
        # Generate questions by category
        general_questions = self.generate_general_questions(general_count)
        skill_questions = self.generate_skill_questions(resume_data.get("skills", []), skill_count)
        missing_skill_questions = self.generate_missing_skill_questions(match_result.get("missing_skills", []), missing_skill_count)
        experience_questions = self.generate_experience_questions(resume_data, experience_count)
        education_questions = self.generate_education_questions(resume_data, education_count)
        
        # Combine all questions
        all_questions.extend(general_questions)
        all_questions.extend(skill_questions)
        all_questions.extend(missing_skill_questions)
        all_questions.extend(experience_questions)
        all_questions.extend(education_questions)
        
        # If we still need more questions, add more general questions
        if len(all_questions) < num_questions:
            additional_general = self.generate_general_questions(num_questions - len(all_questions))
            all_questions.extend(additional_general)
        
        # Shuffle the questions to mix categories
        random.shuffle(all_questions)
        
        # Limit to the requested number of questions
        return all_questions[:num_questions] 