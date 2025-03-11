import torch
import os
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from ..utils.logging import logger, log_performance
from ..config import config

class SummarizerException(Exception):
    """Exception raised for summarizer errors"""
    pass

class Summarizer:
    """Text summarization model wrapper with error handling"""
    
    def __init__(self, model_name=None, cache_dir=None, device=None):
        """
        Initialize the summarizer
        
        Args:
            model_name (str, optional): Name of the model to use
            cache_dir (str, optional): Directory to cache models
            device (str, optional): Device to use for inference ('cpu' or 'cuda')
        """
        self.model_name = model_name or config["model"]["name"]
        self.cache_dir = cache_dir or config["model"]["cache_dir"]
        
        # Create cache directory if it doesn't exist
        if self.cache_dir and not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        # Set device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        
        logger.info(f"Initializing summarizer with model {self.model_name} on {self.device}")
        
        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, cache_dir=self.cache_dir)
            self.model.to(self.device)
            
            # Get model type for prefix handling
            self.is_t5 = "t5" in self.model_name.lower()
            
            logger.info(f"Summarizer initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing summarizer: {str(e)}")
            raise SummarizerException(f"Failed to initialize summarizer: {str(e)}")
    
    @log_performance(logger)
    def generate_summary(self, text, max_length=None, min_length=None, num_beams=4):
        """
        Generate a summary for the given text
        
        Args:
            text (str): Text to summarize
            max_length (int, optional): Maximum summary length
            min_length (int, optional): Minimum summary length
            num_beams (int, optional): Number of beams for beam search
            
        Returns:
            str: Generated summary
            
        Raises:
            SummarizerException: If there's an error during summarization
        """
        if not text:
            logger.warning("Empty text provided for summarization")
            return ""
        
        # Get parameters from config if not provided
        max_length = max_length or config["model"]["max_length"]
        min_length = min_length or config["model"]["min_length"]
        
        try:
            # Add prefix for T5 models
            if self.is_t5:
                text = "summarize: " + text
            
            # Handle text that exceeds model's max token limit
            encoded = self.tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=self.tokenizer.model_max_length)
            encoded = encoded.to(self.device)
            
            # Generate summary
            with torch.no_grad():
                summary_ids = self.model.generate(
                    encoded,
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=num_beams,
                    early_stopping=True,
                    no_repeat_ngram_size=3
                )
            
            # Decode summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            
            logger.info(f"Generated summary of length {len(summary)} characters")
            return summary
            
        except torch.cuda.OutOfMemoryError:
            logger.error("CUDA out of memory error during summarization")
            # Fall back to CPU if CUDA OOM
            if self.device.type == "cuda":
                logger.info("Falling back to CPU for summarization")
                self.model.to("cpu")
                self.device = torch.device("cpu")
                return self.generate_summary(text, max_length, min_length, num_beams)
            else:
                raise SummarizerException("Out of memory error during summarization")
                
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise SummarizerException(f"Failed to generate summary: {str(e)}")
    
    @log_performance(logger)
    def generate_summary_for_long_text(self, text, max_length=None, min_length=None):
        """
        Generate a summary for long text by splitting it into chunks
        
        Args:
            text (str): Long text to summarize
            max_length (int, optional): Maximum summary length
            min_length (int, optional): Minimum summary length
            
        Returns:
            str: Generated summary
        """
        if not text:
            logger.warning("Empty text provided for summarization")
            return ""
        
        try:
            # Get parameters from config if not provided
            max_length = max_length or config["model"]["max_length"]
            min_length = min_length or config["model"]["min_length"]
            
            # Check if text needs to be split
            if len(self.tokenizer.encode(text)) <= self.tokenizer.model_max_length:
                return self.generate_summary(text, max_length, min_length)
            
            # Split text and summarize parts separately
            from ..data.processor import chunk_text
            chunks = chunk_text(text, max_chunk_size=self.tokenizer.model_max_length // 2)
            
            logger.info(f"Text split into {len(chunks)} chunks for summarization")
            
            # Generate summary for each chunk
            chunk_summaries = []
            for i, chunk in enumerate(chunks):
                logger.debug(f"Summarizing chunk {i+1}/{len(chunks)}")
                chunk_summary = self.generate_summary(
                    chunk, 
                    max_length=max(30, max_length // len(chunks)), 
                    min_length=max(10, min_length // len(chunks))
                )
                chunk_summaries.append(chunk_summary)
            
            # Combine chunk summaries
            combined_summary = " ".join(chunk_summaries)
            
            # If the combined summary is still too long, summarize it again
            if len(self.tokenizer.encode(combined_summary)) > self.tokenizer.model_max_length:
                logger.info("Combined summary still too long, summarizing again")
                final_summary = self.generate_summary(combined_summary, max_length, min_length)
                return final_summary
            
            return combined_summary
            
        except Exception as e:
            logger.error(f"Error generating summary for long text: {str(e)}")
            raise SummarizerException(f"Failed to generate summary for long text: {str(e)}")

# Create a singleton instance
summarizer = None

def get_summarizer():
    """Get or create the summarizer instance"""
    global summarizer
    if summarizer is None:
        summarizer = Summarizer()
    return summarizer 