import os
import tempfile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
import io
import base64

def save_uploaded_file(uploaded_file) -> str:
    """
    Save an uploaded file to a temporary location and return the path.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
        
    Returns:
        Path to the saved file
    """
    # Create a temporary file
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    
    # Write the file to the temporary location
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def create_radar_chart(match_result: Dict[str, Any]) -> str:
    """
    Create a radar chart visualization of the match scores.
    
    Args:
        match_result: Dictionary containing match scores
        
    Returns:
        Base64 encoded string of the chart image
    """
    # Extract match scores
    categories = ['Skills', 'Education', 'Experience', 'Overall']
    values = [
        match_result.get('skills_match', 0),
        match_result.get('education_match', 0),
        match_result.get('experience_match', 0),
        match_result.get('overall_match', 0)
    ]
    
    # Number of variables
    N = len(categories)
    
    # What will be the angle of each axis in the plot (divide the plot / number of variables)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Values need to be repeated to close the loop
    values += values[:1]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories, size=12)
    
    # Draw the y-axis labels (0-100)
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], size=10)
    plt.ylim(0, 100)
    
    # Plot the data
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    
    # Fill the area
    ax.fill(angles, values, alpha=0.25)
    
    # Add a title
    plt.title("Resume-Job Match Analysis", size=15, y=1.1)
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode the image to base64
    img_str = base64.b64encode(buf.read()).decode()
    
    # Close the plot to free memory
    plt.close()
    
    return img_str

def create_skills_comparison_chart(resume_skills: List[str], job_skills: List[str]) -> str:
    """
    Create a bar chart comparing resume skills with job required skills.
    
    Args:
        resume_skills: List of skills from the resume
        job_skills: List of skills required in the job description
        
    Returns:
        Base64 encoded string of the chart image
    """
    # Convert to lowercase for case-insensitive matching
    resume_skills_lower = [skill.lower() for skill in resume_skills]
    job_skills_lower = [skill.lower() for skill in job_skills]
    
    # Find matching and missing skills
    matching_skills = [skill for skill in job_skills if skill.lower() in resume_skills_lower]
    missing_skills = [skill for skill in job_skills if skill.lower() not in resume_skills_lower]
    
    # Create a DataFrame for the chart
    df = pd.DataFrame({
        'Skill': matching_skills + missing_skills,
        'Status': ['Match'] * len(matching_skills) + ['Missing'] * len(missing_skills)
    })
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, max(6, len(df) * 0.4)))
    
    # Plot the data
    colors = {'Match': 'green', 'Missing': 'red'}
    for status, group in df.groupby('Status'):
        ax.barh(group['Skill'], [1] * len(group), label=status, color=colors[status])
    
    # Add labels and title
    ax.set_xlabel('Status')
    ax.set_title('Skills Comparison')
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df['Skill'])
    ax.legend()
    
    # Remove x-axis ticks
    ax.set_xticks([])
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode the image to base64
    img_str = base64.b64encode(buf.read()).decode()
    
    # Close the plot to free memory
    plt.close()
    
    return img_str

def format_match_score(score: float) -> Tuple[str, str]:
    """
    Format a match score with a color code based on the score value.
    
    Args:
        score: Match score (0-100)
        
    Returns:
        Tuple containing:
            - Formatted score string
            - Color code for the score
    """
    if score >= 80:
        return f"{score:.1f}%", "green"
    elif score >= 60:
        return f"{score:.1f}%", "orange"
    else:
        return f"{score:.1f}%", "red"

def classify_resume(resume_data: Dict[str, Any]) -> str:
    """
    Classify a resume into a job category based on skills and experience.
    
    Args:
        resume_data: Dictionary containing parsed resume information
        
    Returns:
        Job category classification
    """
    # Define job categories and their associated keywords
    job_categories = {
        "Software Development": [
            "python", "java", "javascript", "html", "css", "react", "angular", "vue", "node.js",
            "django", "flask", "spring", "developer", "software engineer", "programmer", "coding",
            "git", "github", "gitlab", "bitbucket", "agile", "scrum", "devops", "ci/cd"
        ],
        "Data Science": [
            "data science", "machine learning", "deep learning", "artificial intelligence", "ai",
            "ml", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "data analysis",
            "statistics", "r", "data mining", "big data", "data visualization", "tableau", "power bi"
        ],
        "Web Development": [
            "html", "css", "javascript", "react", "angular", "vue", "node.js", "php", "wordpress",
            "web developer", "frontend", "backend", "full stack", "responsive design", "ui/ux",
            "web design", "seo", "cms", "jquery", "bootstrap", "sass", "less"
        ],
        "Marketing": [
            "marketing", "digital marketing", "seo", "sem", "social media", "content marketing",
            "email marketing", "google analytics", "advertising", "brand", "market research",
            "campaign", "customer acquisition", "lead generation", "conversion rate", "copywriting"
        ],
        "Finance": [
            "finance", "accounting", "financial analysis", "budget", "forecasting", "investment",
            "banking", "cpa", "cfa", "excel", "financial modeling", "balance sheet", "income statement",
            "cash flow", "tax", "audit", "risk management", "portfolio management"
        ],
        "Human Resources": [
            "hr", "human resources", "recruiting", "talent acquisition", "onboarding", "training",
            "employee relations", "benefits", "compensation", "performance management", "hris",
            "diversity", "inclusion", "workforce planning", "employee engagement", "hr policies"
        ],
        "Project Management": [
            "project management", "pmp", "agile", "scrum", "kanban", "waterfall", "prince2",
            "project planning", "risk management", "stakeholder management", "project coordination",
            "program management", "project delivery", "gantt", "jira", "asana", "trello"
        ]
    }
    
    # Count matches for each category
    category_scores = {}
    
    # Extract text from resume data
    resume_text = " ".join([
        " ".join(resume_data.get("skills", [])),
        " ".join(resume_data.get("experience", [])),
        " ".join(resume_data.get("education", []))
    ]).lower()
    
    for category, keywords in job_categories.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in resume_text:
                score += 1
        category_scores[category] = score
    
    # Find the category with the highest score
    if category_scores:
        best_category = max(category_scores.items(), key=lambda x: x[1])
        if best_category[1] > 0:
            return best_category[0]
    
    return "General" 