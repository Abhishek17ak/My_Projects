"""
Configuration management for SentimentVault
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_TTL = int(os.getenv("REDIS_TTL", 3600))  # 1 hour

# FastAPI Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Model Configuration
MODEL_PATH = os.getenv("MODEL_PATH", str(MODELS_DIR / "sentiment_model"))
TOKENIZER_PATH = os.getenv("TOKENIZER_PATH", str(MODELS_DIR / "sentiment_model"))
MAX_SEQ_LENGTH = int(os.getenv("MAX_SEQ_LENGTH", 512))

# Data Configuration
TRAIN_SIZE = int(os.getenv("TRAIN_SIZE", 200000))
TEST_SIZE = int(os.getenv("TEST_SIZE", 50000))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 16))
EPOCHS = int(os.getenv("EPOCHS", 3))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", 2e-5))

# Model Configuration
MODEL_NAME = "distilbert-base-uncased"
NUM_LABELS = 2  # Positive/Negative

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
