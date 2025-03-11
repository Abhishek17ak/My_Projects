import streamlit as st
import requests
import json
import os
import time
import pandas as pd
from datetime import datetime

# Set page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Financial Report Summarizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Default configuration
config = {
    "api": {
        "host": "localhost",
        "port": 5000
    },
    "model": {
        "max_length": 200,
        "min_length": 50
    }
}

# API configuration
API_URL = os.getenv("API_URL", f"http://{config['api']['host']}:{config['api']['port']}")
API_KEY = os.getenv("API_KEY", "your_api_key_1")  # Default API key for demo

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
    }
    .success-box {
        padding: 1rem;
        background-color: #E8F5E9;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #4CAF50;
    }
    .info-box {
        padding: 1rem;
        background-color: #E3F2FD;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #2196F3;
    }
    .warning-box {
        padding: 1rem;
        background-color: #FFF8E1;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #FFC107;
    }
    .error-box {
        padding: 1rem;
        background-color: #FFEBEE;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #F44336;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">Financial Report Summarizer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Generate concise summaries from financial reports</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/000000/financial-growth.png", width=100)
st.sidebar.title("Options")

# API configuration in sidebar
api_url = st.sidebar.text_input("API URL", value=API_URL)
api_key = st.sidebar.text_input("API Key", value=API_KEY, type="password")

# Model parameters
st.sidebar.markdown("## Model Parameters")
max_length = st.sidebar.slider("Maximum summary length", 50, 500, config["model"]["max_length"])
min_length = st.sidebar.slider("Minimum summary length", 20, 100, config["model"]["min_length"])

# Health check function
def check_api_health():
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            if health_data["status"] == "healthy":
                st.sidebar.markdown('<div class="success-box">API is healthy</div>', unsafe_allow_html=True)
            else:
                st.sidebar.markdown(f'<div class="warning-box">API health issues: {health_data}</div>', unsafe_allow_html=True)
        else:
            st.sidebar.markdown('<div class="error-box">API health check failed</div>', unsafe_allow_html=True)
    except Exception as e:
        st.sidebar.markdown(f'<div class="error-box">API connection error: {str(e)}</div>', unsafe_allow_html=True)

# Check API health
check_api_health()

# Main content
tab1, tab2, tab3 = st.tabs(["Text Input", "File Upload", "SEC EDGAR"])

# Text Input Tab
with tab1:
    st.markdown("### Enter Financial Text")
    text_area = st.text_area("Paste financial text here:", height=300)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        generate_button = st.button("Generate Summary", type="primary")
    
    if generate_button and text_area:
        with st.spinner("Generating summary..."):
            try:
                start_time = time.time()
                
                response = requests.post(
                    f"{api_url}/summarizer/summarize",
                    headers={"X-API-Key": api_key, "Content-Type": "application/json"},
                    json={"text": text_area, "max_length": max_length, "min_length": min_length},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown("### Summary")
                    st.markdown(f'<div class="info-box">{result["summary"]}</div>', unsafe_allow_html=True)
                    
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Original Length", f"{result['original_length']} chars")
                    col2.metric("Summary Length", f"{result['summary_length']} chars")
                    col3.metric("Compression Ratio", f"{result['original_length'] / result['summary_length']:.1f}x")
                    
                    st.markdown(f"Processing time: {result.get('processing_time', time.time() - start_time):.2f} seconds")
                    
                    # Copy button
                    st.download_button(
                        label="Download Summary",
                        data=result["summary"],
                        file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                else:
                    error_msg = "Unknown error"
                    try:
                        error_data = response.json()
                        error_msg = error_data.get("error", "Unknown error")
                    except:
                        pass
                    
                    st.markdown(f'<div class="error-box">Error: {error_msg}</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown(f'<div class="error-box">Error: {str(e)}</div>', unsafe_allow_html=True)
    elif generate_button:
        st.warning("Please enter some text to summarize")

# File Upload Tab
with tab2:
    st.markdown("### Upload Financial Document")
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])
    
    if uploaded_file is not None:
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": f"{uploaded_file.size / 1024:.2f} KB"}
        st.write(file_details)
        
        try:
            # For simplicity, we're only handling text files here
            if uploaded_file.type == "text/plain":
                text_content = uploaded_file.getvalue().decode("utf-8")
                
                if len(text_content) > 1000:
                    st.markdown(f"Preview: {text_content[:1000]}...")
                else:
                    st.markdown(f"Preview: {text_content}")
                
                if st.button("Generate Summary from File", type="primary"):
                    with st.spinner("Generating summary..."):
                        try:
                            response = requests.post(
                                f"{api_url}/summarizer/summarize",
                                headers={"X-API-Key": api_key, "Content-Type": "application/json"},
                                json={"text": text_content, "max_length": max_length, "min_length": min_length},
                                timeout=60
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                
                                st.markdown("### Summary")
                                st.markdown(f'<div class="info-box">{result["summary"]}</div>', unsafe_allow_html=True)
                                
                                # Metrics
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Original Length", f"{result['original_length']} chars")
                                col2.metric("Summary Length", f"{result['summary_length']} chars")
                                col3.metric("Compression Ratio", f"{result['original_length'] / result['summary_length']:.1f}x")
                            else:
                                st.error(f"Error: {response.text}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.warning("Currently only supporting text files. PDF and DOCX support coming soon!")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# SEC EDGAR Tab
with tab3:
    st.markdown("### Fetch from SEC EDGAR")
    
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("Company Ticker Symbol (e.g., AAPL)")
    with col2:
        year = st.number_input("Year", min_value=2000, max_value=datetime.now().year, value=2022)
    
    if st.button("Fetch 10-K Filing", type="primary") and ticker:
        st.info(f"This would fetch the 10-K filing for {ticker} ({year}) from SEC EDGAR.")
        st.warning("SEC EDGAR integration is a placeholder in this demo.")
        
        # Sample for demo
        st.markdown("### Sample 10-K Preview")
        sample_text = f"This is a sample 10-K filing for {ticker} from {year}. In a real application, this would contain the actual text fetched from SEC EDGAR."
        st.text_area("Preview", sample_text, height=200)
        
        if st.button("Generate Summary from SEC Filing"):
            st.warning("This is a placeholder. In a production app, this would generate a summary of the actual filing.")

# Footer
st.markdown("---")
st.markdown("Financial Report Summarizer | Powered by AI | © 2023") 