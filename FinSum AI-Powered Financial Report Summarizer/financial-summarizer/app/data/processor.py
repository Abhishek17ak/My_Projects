import re
import nltk
from nltk.tokenize import sent_tokenize
from ..utils.logging import logger, log_performance

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

@log_performance(logger)
def preprocess_financial_text(text):
    """
    Clean and preprocess financial report text
    
    Args:
        text (str): Raw text from financial report
        
    Returns:
        str: Preprocessed text
    """
    if not text:
        logger.warning("Empty text provided for preprocessing")
        return ""
    
    try:
        # Remove headers, footers, and page numbers
        text = re.sub(r'Page \d+ of \d+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove common disclaimers
        text = re.sub(r'This document contains forward-looking statements.*?risks and uncertainties\.', 
                     '', text, flags=re.DOTALL)
        
        # Remove table of contents sections
        text = re.sub(r'Table of Contents.*?Item 1\.', 'Item 1.', text, flags=re.DOTALL)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
                     '', text)
        
        logger.info(f"Preprocessed text from {len(text)} characters")
        return text
    
    except Exception as e:
        logger.error(f"Error preprocessing text: {str(e)}")
        # Return original text if preprocessing fails
        return text

@log_performance(logger)
def segment_into_sections(text):
    """
    Identify and extract common sections from financial reports
    
    Args:
        text (str): Preprocessed text
        
    Returns:
        dict: Dictionary with section names as keys and section text as values
    """
    if not text:
        logger.warning("Empty text provided for segmentation")
        return {}
    
    try:
        # Identify common section headers in financial reports
        section_patterns = [
            r'Management\'s Discussion and Analysis',
            r'Results of Operations',
            r'Financial Condition',
            r'Risk Factors',
            r'Executive Summary',
            r'Business Overview',
            r'Liquidity and Capital Resources',
            r'Critical Accounting Policies'
        ]
        
        sections = {}
        current_pos = 0
        
        for pattern in section_patterns:
            match = re.search(pattern, text[current_pos:], re.IGNORECASE)
            if match:
                start_pos = current_pos + match.start()
                
                # Find the next section or end of text
                next_section_match = None
                for next_pattern in section_patterns:
                    next_match = re.search(next_pattern, text[start_pos + len(pattern):], re.IGNORECASE)
                    if next_match and (next_section_match is None or next_match.start() < next_section_match.start()):
                        next_section_match = next_match
                
                if next_section_match:
                    end_pos = start_pos + len(pattern) + next_section_match.start()
                else:
                    end_pos = len(text)
                
                sections[pattern] = text[start_pos:end_pos].strip()
                current_pos = end_pos
        
        logger.info(f"Segmented text into {len(sections)} sections")
        return sections
    
    except Exception as e:
        logger.error(f"Error segmenting text: {str(e)}")
        return {}

@log_performance(logger)
def chunk_text(text, max_chunk_size=1024):
    """
    Split text into manageable chunks for processing
    
    Args:
        text (str): Text to chunk
        max_chunk_size (int): Maximum chunk size in characters
        
    Returns:
        list: List of text chunks
    """
    if not text:
        logger.warning("Empty text provided for chunking")
        return []
    
    try:
        # Split into sentences
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed max size, start a new chunk
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += " " + sentence
            else:
                # Save current chunk if not empty
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        # Add the last chunk if not empty
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks
    
    except Exception as e:
        logger.error(f"Error chunking text: {str(e)}")
        # Return the original text as a single chunk if chunking fails
        return [text]

@log_performance(logger)
def process_filing(filing_data):
    """
    Process a single filing through the entire pipeline
    
    Args:
        filing_data (dict): Dictionary with ticker, year, and text
        
    Returns:
        list: List of processed chunks with metadata
    """
    processed_data = []
    
    try:
        # Preprocess the text
        clean_text = preprocess_financial_text(filing_data['text'])
        
        # Segment into sections
        sections = segment_into_sections(clean_text)
        
        # Process each section
        for section_name, section_text in sections.items():
            # Split into manageable chunks
            chunks = chunk_text(section_text)
            
            # Add each chunk to processed data
            for i, chunk in enumerate(chunks):
                processed_data.append({
                    'ticker': filing_data['ticker'],
                    'year': filing_data['year'],
                    'section': section_name,
                    'chunk_id': i,
                    'text': chunk,
                    'content_hash': filing_data.get('content_hash', '')
                })
        
        logger.info(f"Processed filing for {filing_data['ticker']} ({filing_data['year']})")
        return processed_data
    
    except Exception as e:
        logger.error(f"Error processing filing for {filing_data.get('ticker', 'unknown')}: {str(e)}")
        return [] 