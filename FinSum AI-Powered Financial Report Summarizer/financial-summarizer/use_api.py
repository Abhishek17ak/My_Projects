import requests
import json

# API configuration
API_URL = "http://localhost:5000"
API_KEY = "your_api_key_1"

# Sample financial text
sample_text = """
Financial report for Q3 2023: Revenue increased by 15% year-over-year to $2.5 billion, 
driven by strong performance in our cloud services division which grew 32%. 
Operating margin improved to 28% from 24% in the same period last year. 
Net income was $580 million, up 22% from Q3 2022. 
Cash flow from operations was $720 million. 
We invested $150 million in R&D and completed the acquisition of TechSolutions Inc. for $300 million. 
Our balance sheet remains strong with $3.2 billion in cash and short-term investments. 
Looking ahead, we expect continued growth in Q4 with full-year revenue guidance raised to $9.8-10.1 billion.
"""

def summarize_text(text):
    """Send text to the API for summarization"""
    try:
        response = requests.post(
            f"{API_URL}/summarizer/summarize",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"text": text},
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"

def check_health():
    """Check the health of the API"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"

if __name__ == "__main__":
    print("Checking API health...")
    health = check_health()
    print(json.dumps(health, indent=2))
    
    print("\nSummarizing sample text...")
    result = summarize_text(sample_text)
    print(json.dumps(result, indent=2)) 