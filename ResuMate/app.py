import streamlit as st
import PyPDF2
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import re

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

def extract_skills(text, nlp):
    """Extract skills from text using spaCy and predefined skill patterns."""
    # Define skill categories and their patterns
    skill_patterns = {
        "Programming Languages": [
            "python", "java", "javascript", "typescript", "c\\+\\+", "ruby", "php", "swift",
            "kotlin", "rust", "golang", "scala", "r", "matlab"
        ],
        "Machine Learning & AI": [
            "machine learning", "deep learning", "neural networks", "natural language processing",
            "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn", "nlp",
            "artificial intelligence", "ml", "ai", "transformers", "lstm", "cnn"
        ],
        "Data Science": [
            "data science", "data analysis", "statistics", "pandas", "numpy", "matplotlib",
            "data visualization", "jupyter", "feature engineering", "data mining",
            "data modeling", "regression", "classification"
        ],
        "Cloud & DevOps": [
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "ci/cd", "git",
            "terraform", "ansible", "cloud computing", "devops", "mlops"
        ],
        "Big Data": [
            "hadoop", "spark", "kafka", "hive", "pig", "nosql", "mongodb", "cassandra",
            "big data", "data warehouse", "etl", "data pipeline"
        ],
        "Web Technologies": [
            "react", "angular", "vue", "node.js", "django", "flask", "fastapi",
            "rest api", "graphql", "html", "css", "sql"
        ],
        "Soft Skills": [
            "leadership", "communication", "teamwork", "problem solving",
            "project management", "agile", "scrum", "mentoring"
        ]
    }

    found_skills = {category: [] for category in skill_patterns}
    
    # Convert text to lowercase for matching
    text_lower = text.lower()
    
    # Find skills in each category
    for category, patterns in skill_patterns.items():
        for skill in patterns:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills[category].append(skill)
    
    return found_skills

def calculate_match_score(resume_skills, job_skills):
    """Calculate match score based on skills overlap."""
    total_required = 0
    total_matched = 0
    
    for category in job_skills:
        if job_skills[category]:  # If category has any skills
            total_required += len(job_skills[category])
            for skill in job_skills[category]:
                if skill in resume_skills.get(category, []):
                    total_matched += 1
    
    return (total_matched / total_required * 100) if total_required > 0 else 0

def identify_missing_skills(resume_skills, job_skills):
    """Identify skills present in job description but missing from resume."""
    missing_skills = {}
    
    for category in job_skills:
        if job_skills[category]:  # If category has any skills
            missing = [skill for skill in job_skills[category] 
                      if skill not in resume_skills.get(category, [])]
            if missing:
                missing_skills[category] = missing
    
    return missing_skills

def main():
    st.set_page_config(page_title="Resume Skills Matcher", layout="wide")
    st.title("Resume Skills Matcher")
    
    # Load spaCy model
    try:
        nlp = spacy.load("en_core_web_lg")
    except:
        st.error("Please install the spaCy model: python -m spacy download en_core_web_lg")
        return
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # Resume upload section
    with col1:
        st.subheader("Resume Upload")
        resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    
    # Job description section
    with col2:
        st.subheader("Job Description")
        job_description = st.text_area("Paste job description here", height=300)
    
    # Analysis button
    if st.button("Analyze Match") and resume_file and job_description:
        with st.spinner("Analyzing..."):
            # Extract text from resume
            resume_text = extract_text_from_file(resume_file)
            
            if resume_text:
                # Extract skills
                resume_skills = extract_skills(resume_text, nlp)
                job_skills = extract_skills(job_description, nlp)
                
                # Calculate match score
                match_score = calculate_match_score(resume_skills, job_skills)
                
                # Find missing skills
                missing_skills = identify_missing_skills(resume_skills, job_skills)
                
                # Display results
                st.divider()
                
                # Display match score with color
                st.header("Skills Match Analysis")
                score_color = "green" if match_score >= 70 else "orange" if match_score >= 50 else "red"
                st.markdown(f"<h2 style='color: {score_color}'>Skills Match Score: {match_score:.1f}%</h2>", 
                          unsafe_allow_html=True)
                
                # Display skills comparison
                st.subheader("Skills Analysis by Category")
                
                for category in job_skills:
                    if job_skills[category]:  # If category has any required skills
                        st.write(f"\n**{category}**")
                        for skill in job_skills[category]:
                            if skill in resume_skills.get(category, []):
                                st.markdown(f"✅ {skill}")
                            else:
                                st.markdown(f"❌ {skill}")
                
                # Display missing skills summary
                if missing_skills:
                    st.subheader("Missing Skills Summary")
                    for category, skills in missing_skills.items():
                        if skills:  # If category has missing skills
                            st.write(f"**{category}:**")
                            st.write(", ".join(skills))
            else:
                st.error("Could not extract text from the uploaded file.")

if __name__ == "__main__":
    main() 