# Resume Screening Assistant

A web-based application that helps recruiters and job seekers match resumes with job descriptions using Natural Language Processing (NLP) and Machine Learning techniques.

## Features

- Resume parsing from PDF and DOCX formats
- Job description analysis
- Resume-job matching with similarity scoring
- Skill gap identification
- Automated interview question generation
- Resume classification by job role
- Resume improvement suggestions

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd resume-screening-assistant
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Download the spaCy language model (if not automatically installed):
   ```
   python -m spacy download en_core_web_lg
   ```

### Running the Application

Start the Streamlit web application:
```
streamlit run app.py
```

The application will be available at http://localhost:8501 in your web browser.

## Usage

1. Upload a resume in PDF or DOCX format
2. Enter or paste a job description
3. Click "Analyze" to process the resume and job description
4. View the match score, missing skills, and suggested interview questions
5. Use the additional features to improve the resume or refine the matching criteria

## Project Structure

- `app.py`: Main Streamlit application
- `resume_parser.py`: Module for extracting information from resumes
- `job_parser.py`: Module for analyzing job descriptions
- `matcher.py`: Algorithms for matching resumes with job descriptions
- `interview_generator.py`: Module for generating interview questions
- `utils.py`: Utility functions for text processing and visualization

## License

MIT 