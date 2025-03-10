import streamlit as st
import PyPDF2
import docx
from resume_parser import ResumeParser
from job_parser import JobParser
from matcher import ResumeJobMatcher

def read_pdf(file):
    """Read text from PDF file."""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

def read_docx(file):
    """Read text from DOCX file."""
    text = ""
    try:
        doc = docx.Document(file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
    return text

def format_salary(salary_info):
    """Format salary information for display."""
    if not salary_info:
        return "Not specified"
    
    min_salary = f"${salary_info['min']:,.0f}"
    max_salary = f"${salary_info['max']:,.0f}"
    
    if salary_info.get("original"):
        # Show both hourly and annual
        orig = salary_info["original"]
        return f"${orig['min']:.2f} - ${orig['max']:.2f}/hour ({min_salary} - {max_salary}/year)"
    else:
        return f"{min_salary} - {max_salary}/year"

def main():
    st.set_page_config(page_title="Advanced Resume Matcher", layout="wide")
    
    # Initialize parsers and matcher
    resume_parser = ResumeParser()
    job_parser = JobParser()
    matcher = ResumeJobMatcher()
    
    st.title("Advanced Resume Matcher")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # Resume upload section
    with col1:
        st.subheader("Resume Upload")
        resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
        
        if resume_file:
            # Read resume file
            if resume_file.type == "application/pdf":
                resume_text = read_pdf(resume_file)
            else:
                resume_text = read_docx(resume_file)
            
            if resume_text:
                resume_data = resume_parser.parse_resume(resume_text)
    
    # Job description section
    with col2:
        st.subheader("Job Description")
        job_description = st.text_area("Paste job description here", height=300)
        
        if job_description:
            job_data = job_parser.parse_job_description(job_description)
    
    # Analysis button
    if st.button("Analyze Match") and resume_file and job_description:
        st.divider()
        
        # Calculate match score
        match_results = matcher.calculate_match_score(resume_data, job_data)
        overall_score = match_results["overall_score"]
        
        # Display overall match score
        st.header("Match Analysis")
        st.metric("Overall Match Score", f"{overall_score:.1f}%")
        
        # Create three columns for detailed scores
        score_col1, score_col2, score_col3 = st.columns(3)
        
        # Skills score
        with score_col1:
            skills_score = match_results["component_scores"]["skills"]["overall_score"]
            st.metric("Skills Match", f"{skills_score:.1f}%")
        
        # Education score
        with score_col2:
            education_score = match_results["component_scores"]["education"]["score"]
            st.metric("Education Match", f"{education_score:.1f}%")
        
        # Experience score
        with score_col3:
            experience_score = match_results["component_scores"]["experience"]["score"]
            st.metric("Experience Match", f"{experience_score:.1f}%")
        
        st.divider()
        
        # Detailed Analysis Section
        st.subheader("Detailed Analysis")
        
        # Missing Skills
        if match_results["missing_skills"]:
            st.write("**Missing Skills:**")
            for category, skills in match_results["missing_skills"].items():
                if skills:
                    st.write(f"- {category.title()}: {', '.join(skills)}")
        
        # Experience Analysis
        exp_details = match_results["component_scores"]["experience"]["details"]
        st.write("**Experience Analysis:**")
        st.write(f"- Your experience: {exp_details['years_match']['resume_years']:.1f} years")
        st.write(f"- Required: {exp_details['years_match']['required_years']:.1f} years")
        if exp_details['years_match'].get('preferred_years'):
            st.write(f"- Preferred: {exp_details['years_match']['preferred_years']:.1f} years")
        
        # Education Analysis
        edu_details = match_results["component_scores"]["education"]["details"]
        st.write("**Education Analysis:**")
        if job_data["education"]["required_degree"]:
            st.write(f"- Required degree: {job_data['education']['required_degree'].title()}")
        if job_data["education"]["fields"]:
            st.write(f"- Desired fields: {', '.join(job_data['education']['fields'])}")
        
        # Salary Information
        if job_data["salary"]:
            st.write("**Salary Range:**")
            st.write(format_salary(job_data["salary"]))
        
        st.divider()
        
        # Improvement Suggestions
        if match_results["improvement_suggestions"]:
            st.subheader("Improvement Suggestions")
            for suggestion in match_results["improvement_suggestions"]:
                st.write(f"- {suggestion}")

if __name__ == "__main__":
    main() 