import streamlit as st
import PyPDF2
import docx
import re
import spacy
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Cover Letter Generator",
    page_icon="📝",
    layout="wide"
)

# Custom CSS for footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f8f9fa;
    color: #6c757d;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #dee2e6;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_nlp_model():
    """Load spaCy model for text processing."""
    try:
        return spacy.load("en_core_web_sm")
    except:
        st.warning("Downloading spaCy model. This may take a moment...")
        import subprocess
        subprocess.run([f"{sys.executable}", "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

def extract_text_from_file(uploaded_file):
    """Extract text from PDF or DOCX file."""
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
    return None

def extract_resume_info(text, nlp):
    """Extract key information from resume text."""
    doc = nlp(text)
    
    # Extract name (assuming it's at the beginning of the resume)
    name_pattern = re.compile(r'^([A-Z][a-z]+ [A-Z][a-z]+)')
    name_match = name_pattern.search(text.strip())
    name = name_match.group(1) if name_match else "Applicant"
    
    # Extract skills (simple keyword matching)
    skills = []
    skill_keywords = [
        "python", "java", "javascript", "typescript", "c++", "ruby", "php", "swift",
        "kotlin", "rust", "golang", "sql", "nosql", "mongodb", "postgresql", "mysql",
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "terraform",
        "react", "angular", "vue", "node.js", "django", "flask", "spring", "tensorflow",
        "pytorch", "scikit-learn", "pandas", "numpy", "hadoop", "spark", "kafka",
        "leadership", "communication", "teamwork", "problem solving", "critical thinking",
        "time management", "project management", "agile", "scrum"
    ]
    
    text_lower = text.lower()
    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            skills.append(skill)
    
    # Extract experience (simple approach)
    experience_section = ""
    lines = text.split('\n')
    in_experience_section = False
    
    for line in lines:
        if re.search(r'\b(EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT)\b', line, re.IGNORECASE):
            in_experience_section = True
            continue
        elif re.search(r'\b(EDUCATION|SKILLS|PROJECTS)\b', line, re.IGNORECASE) and in_experience_section:
            break
        
        if in_experience_section:
            experience_section += line + "\n"
    
    # Extract education
    education_section = ""
    lines = text.split('\n')
    in_education_section = False
    
    for line in lines:
        if re.search(r'\b(EDUCATION|ACADEMIC|DEGREE)\b', line, re.IGNORECASE):
            in_education_section = True
            continue
        elif re.search(r'\b(EXPERIENCE|SKILLS|PROJECTS|CERTIFICATIONS)\b', line, re.IGNORECASE) and in_education_section:
            break
        
        if in_education_section:
            education_section += line + "\n"
    
    # Extract achievements
    achievements = []
    bullet_pattern = re.compile(r'[•●■◆-]\s*(.*?)(?=\n|$)')
    bullet_matches = bullet_pattern.findall(text)
    
    for match in bullet_matches:
        if len(match.strip()) > 20:  # Only consider substantial bullet points
            achievements.append(match.strip())
    
    return {
        "name": name,
        "skills": skills,
        "experience": experience_section.strip(),
        "education": education_section.strip(),
        "achievements": achievements[:3],  # Take top 3 achievements
        "full_text": text
    }

def extract_job_info(job_description):
    """Extract key information from job description."""
    # Extract required skills
    required_skills = []
    skill_keywords = [
        "python", "java", "javascript", "typescript", "c++", "ruby", "php", "swift",
        "kotlin", "rust", "golang", "sql", "nosql", "mongodb", "postgresql", "mysql",
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "terraform",
        "react", "angular", "vue", "node.js", "django", "flask", "spring", "tensorflow",
        "pytorch", "scikit-learn", "pandas", "numpy", "hadoop", "spark", "kafka",
        "leadership", "communication", "teamwork", "problem solving", "critical thinking",
        "time management", "project management", "agile", "scrum"
    ]
    
    job_lower = job_description.lower()
    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', job_lower):
            required_skills.append(skill)
    
    return {
        "required_skills": required_skills
    }

def generate_cover_letter(resume_info, job_info, company_name, job_title):
    """Generate a professional cover letter based on resume and job information."""
    # Get current date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Find matching skills
    matching_skills = [skill for skill in resume_info["skills"] if skill in job_info["required_skills"]]
    if not matching_skills and resume_info["skills"]:
        matching_skills = resume_info["skills"][:5]
    
    # Format achievements
    achievements_text = ""
    if resume_info["achievements"]:
        achievements_text = "In my previous roles, I have:\n"
        for achievement in resume_info["achievements"]:
            achievements_text += f"• {achievement}\n"
    else:
        achievements_text = "Throughout my career, I have consistently demonstrated my ability to deliver high-quality results, work effectively in team environments, and adapt to new technologies."
    
    # Create a structured cover letter
    cover_letter = f"""
{today}

Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company_name}. With my background in {', '.join(matching_skills[:3]) if matching_skills else 'relevant fields'}, I am confident that I would be a valuable addition to your team.

{achievements_text}

My technical skills include {', '.join(resume_info['skills'][3:8]) if len(resume_info['skills']) > 3 else ', '.join(resume_info['skills'])}. These skills align well with the requirements outlined in your job description. I am particularly drawn to {company_name} because of its reputation for excellence in the industry, and I am excited about the opportunity to contribute to your team's success.

My professional experience has equipped me with the necessary skills to excel in this role. I believe my background in {', '.join(matching_skills[:3]) if matching_skills else 'this field'} would allow me to make an immediate impact at {company_name}.

I would appreciate the opportunity to further discuss how my qualifications align with your needs for the {job_title} position. Thank you for your time and consideration.

Sincerely,
{resume_info['name']}
"""
    
    return cover_letter.strip()

def main():
    st.title("📝 Professional Cover Letter Generator")
    st.markdown("""
    Upload your resume and paste a job description to generate a personalized cover letter.
    """)
    
    # Load models
    nlp = load_nlp_model()
    
    # Create two columns for the main inputs
    col1, col2 = st.columns(2)
    
    # Resume upload section
    with col1:
        st.subheader("Resume Upload")
        resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    
    # Job description section
    with col2:
        st.subheader("Job Description")
        job_description = st.text_area("Paste job description here", height=300)
    
    # Create two columns for company and position inputs
    col3, col4 = st.columns(2)
    
    # Company name input
    with col3:
        company_name = st.text_input("Company Name", "")
        st.caption("Enter the company name you're applying to")
    
    # Position title input
    with col4:
        job_title = st.text_input("Position Title", "")
        st.caption("Enter the position title you're applying for")
    
    # Generate button
    if st.button("Generate Cover Letter") and resume_file and job_description:
        if not company_name:
            st.warning("Please enter a company name.")
            return
        
        if not job_title:
            st.warning("Please enter a position title.")
            return
            
        with st.spinner("Processing resume and generating cover letter..."):
            # Extract text from resume
            resume_text = extract_text_from_file(resume_file)
            
            if resume_text:
                # Extract resume information
                resume_info = extract_resume_info(resume_text, nlp)
                
                # Extract job information
                job_info = extract_job_info(job_description)
                
                # Generate cover letter
                cover_letter = generate_cover_letter(resume_info, job_info, company_name, job_title)
                
                # Display results
                st.divider()
                st.subheader("Your Generated Cover Letter")
                
                # Display in a text area that can be edited
                edited_cover_letter = st.text_area("Edit your cover letter as needed:", value=cover_letter, height=400)
                
                # Download button
                st.download_button(
                    label="Download Cover Letter",
                    data=edited_cover_letter,
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )
            else:
                st.error("Could not extract text from the uploaded file.")
    
    # Footer with attribution
    st.markdown("""
    <div class="footer">
        Developed by Abhishek Kalugade © 2023 | <a href="https://github.com/abhishekkalugade/cover-letter-generator" target="_blank">GitHub</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    import sys
    main() 