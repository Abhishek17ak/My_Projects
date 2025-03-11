import streamlit as st
import time
from datetime import datetime
import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Set page configuration
st.set_page_config(
    page_title="Financial Report Summarizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .info-box {
        padding: 1rem;
        background-color: #E3F2FD;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">Financial Report Summarizer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Generate concise summaries from financial reports</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/000000/financial-growth.png", width=100)
st.sidebar.title("Options")

# Model parameters
st.sidebar.markdown("## Model Parameters")
max_length = st.sidebar.slider("Maximum summary length", 50, 500, 200)
min_length = st.sidebar.slider("Minimum summary length", 20, 100, 50)

# Initialize model
@st.cache_resource
def load_model():
    try:
        with st.spinner("Loading model... This may take a minute."):
            # Use a smaller model for faster loading
            model_name = "t5-small"  # Using t5-small instead of t5-base for faster loading
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

# Generate summary
def generate_summary(text, max_length=200, min_length=50):
    if len(text) < 100:
        return "Text is too short to summarize. Please provide a longer text."
    
    try:
        tokenizer, model = load_model()
        if tokenizer is None or model is None:
            return "Model failed to load. Please try again."
        
        # Preprocess text
        sentences = nltk.sent_tokenize(text)
        
        # Prepare input
        inputs = tokenizer("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        
        # Generate summary
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Main content
tab1, tab2 = st.tabs(["Text Input", "File Upload"])

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
                
                summary = generate_summary(text_area, max_length, min_length)
                
                st.markdown("### Summary")
                st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Original Length", f"{len(text_area)} chars")
                col2.metric("Summary Length", f"{len(summary)} chars")
                col3.metric("Compression Ratio", f"{len(text_area) / len(summary):.1f}x")
                
                st.markdown(f"Processing time: {time.time() - start_time:.2f} seconds")
                
                # Copy button
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")
    elif generate_button:
        st.warning("Please enter some text to summarize")

# File Upload Tab
with tab2:
    st.markdown("### Upload Financial Document")
    uploaded_file = st.file_uploader("Choose a file", type=["txt"])
    
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
                            start_time = time.time()
                            
                            summary = generate_summary(text_content, max_length, min_length)
                            
                            st.markdown("### Summary")
                            st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
                            
                            # Metrics
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Original Length", f"{len(text_content)} chars")
                            col2.metric("Summary Length", f"{len(summary)} chars")
                            col3.metric("Compression Ratio", f"{len(text_content) / len(summary):.1f}x")
                            
                            st.markdown(f"Processing time: {time.time() - start_time:.2f} seconds")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.warning("Currently only supporting text files.")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Financial Report Summarizer | Powered by AI | © 2023") 