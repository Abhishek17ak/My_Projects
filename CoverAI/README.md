# Cover Letter Generator

A professional cover letter generator built with Streamlit that creates personalized cover letters based on your resume and job descriptions.

## Features

- **Resume Analysis**: Extracts skills, experience, and achievements from your resume
- **Job Description Analysis**: Identifies required skills from job descriptions
- **Personalized Cover Letters**: Generates tailored cover letters that match your skills to job requirements
- **User-Friendly Interface**: Simple, intuitive interface for uploading documents and generating cover letters
- **Customization**: Edit generated cover letters before downloading

## Live Demo

Try the application live on Streamlit Cloud: [Cover Letter Generator](https://cover-letter-generator.streamlit.app/)

## How to Use

1. Upload your resume (PDF or DOCX format)
2. Paste the job description
3. Enter the company name and position title
4. Click "Generate Cover Letter"
5. Edit the generated cover letter as needed
6. Download the final version

## Local Installation

To run this application locally:

1. Clone the repository:
   ```
   git clone https://github.com/abhishekkalugade/cover-letter-generator.git
   cd cover-letter-generator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   streamlit run app.py
   ```

5. Open your browser and go to http://localhost:8501

## Technologies Used

- **Streamlit**: For the web interface
- **spaCy**: For natural language processing
- **PyPDF2**: For PDF parsing
- **python-docx**: For DOCX parsing

## License

MIT License

## Author

Developed by Abhishek Kalugade

---

Feel free to contribute to this project by submitting issues or pull requests! 
