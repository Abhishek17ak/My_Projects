import streamlit as st
import nltk
import numpy as np
import networkx as nx
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import time
from datetime import datetime

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

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
st.sidebar.markdown("## Parameters")
summary_ratio = st.sidebar.slider("Summary Length (% of original)", 10, 50, 30)

# Generate summary using TextRank algorithm (extractive summarization)
def generate_summary(text, ratio=0.3):
    if len(text) < 100:
        return "Text is too short to summarize. Please provide a longer text."
    
    try:
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # If there are very few sentences, return the text as is
        if len(sentences) <= 3:
            return text
        
        # Remove stopwords and create word vectors
        stop_words = set(stopwords.words('english'))
        
        # Create sentence vectors
        sentence_vectors = []
        for sentence in sentences:
            words = [word.lower() for word in word_tokenize(sentence) if word.isalnum() and word.lower() not in stop_words]
            if not words:
                sentence_vectors.append(np.zeros((1,)))
                continue
                
            # Simple bag of words representation
            vector = np.zeros((len(words),))
            for i, word in enumerate(words):
                vector[i] = 1  # Simple presence encoding
            sentence_vectors.append(vector)
        
        # Create similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j and len(sentence_vectors[i]) > 0 and len(sentence_vectors[j]) > 0:
                    # Use simple overlap for similarity
                    similarity_matrix[i][j] = len(set(word_tokenize(sentences[i].lower())) & 
                                                 set(word_tokenize(sentences[j].lower()))) / \
                                             (len(set(word_tokenize(sentences[i].lower()))) + 
                                              len(set(word_tokenize(sentences[j].lower()))) + 0.001)
        
        # Apply PageRank algorithm
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph)
        
        # Sort sentences by score and select top sentences
        ranked_sentences = sorted(((scores[i], i, s) for i, s in enumerate(sentences)), reverse=True)
        
        # Select top sentences based on the ratio
        num_sentences = max(3, int(len(sentences) * ratio))
        selected_sentences = sorted(ranked_sentences[:num_sentences], key=lambda x: x[1])
        
        # Combine selected sentences
        summary = " ".join([s for _, _, s in selected_sentences])
        
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
                
                summary = generate_summary(text_area, ratio=summary_ratio/100)
                
                st.markdown("### Summary")
                st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Original Length", f"{len(text_area)} chars")
                col2.metric("Summary Length", f"{len(summary)} chars")
                col3.metric("Compression Ratio", f"{len(text_area) / max(1, len(summary)):.1f}x")
                
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
                            
                            summary = generate_summary(text_content, ratio=summary_ratio/100)
                            
                            st.markdown("### Summary")
                            st.markdown(f'<div class="info-box">{summary}</div>', unsafe_allow_html=True)
                            
                            # Metrics
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Original Length", f"{len(text_content)} chars")
                            col2.metric("Summary Length", f"{len(summary)} chars")
                            col3.metric("Compression Ratio", f"{len(text_content) / max(1, len(summary)):.1f}x")
                            
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