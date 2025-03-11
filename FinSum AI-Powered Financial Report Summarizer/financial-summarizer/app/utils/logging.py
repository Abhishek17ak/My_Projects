import logging
import os
import time
from logging.handlers import RotatingFileHandler
from ..config import config

def setup_logging(name="financial_summarizer"):
    """Configure logger with console and file handlers with rotation"""
    
    # Create logs directory if it doesn't exist
    log_file = config["logging"]["file"]
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Get log level from config
    log_level_name = config["logging"]["level"]
    log_level = getattr(logging, log_level_name)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Remove existing handlers if any
    if logger.handlers:
        logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=config["logging"]["max_size"],
        backupCount=config["logging"]["backup_count"]
    )
    file_handler.setLevel(log_level)
    
    # Formatting
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Create a performance tracking decorator
def log_performance(logger):
    """Decorator to log function execution time"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.debug(f"Starting {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                processing_time = time.time() - start_time
                logger.info(f"{func.__name__} completed in {processing_time:.2f}s")
                return result
            except Exception as e:
                processing_time = time.time() - start_time
                logger.error(f"{func.__name__} failed after {processing_time:.2f}s: {str(e)}")
                raise
                
        return wrapper
    return decorator

# Create the logger instance
logger = setup_logging() 