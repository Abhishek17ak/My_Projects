import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config():
    """Load configuration from file and environment variables"""
    # Default configuration
    config = {
        "api": {
            "host": "0.0.0.0",
            "port": 5000,
            "debug": False,
            "workers": 4
        },
        "model": {
            "name": "t5-base",
            "max_length": 150,
            "min_length": 40,
            "cache_dir": "./models/cache"
        },
        "database": {
            "url": "sqlite:///financial_summaries.db"
        },
        "logging": {
            "level": "INFO",
            "file": "financial_summarizer.log",
            "max_size": 10485760,  # 10MB
            "backup_count": 5
        },
        "sec_edgar": {
            "user_agent": "Financial Summarizer App yourname@example.com",
            "max_retries": 3,
            "timeout": 30,
            "backoff_factor": 2
        }
    }
    
    # Load from config file if exists
    config_file = os.getenv("CONFIG_FILE", "config.yaml")
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_file)
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            file_config = yaml.safe_load(f)
            # Update config with file values
            for section, values in file_config.items():
                if section == "environments":
                    continue  # Handle environments separately
                if section in config:
                    config[section].update(values)
                else:
                    config[section] = values
    
    # Apply environment-specific configuration
    env = os.getenv("FLASK_ENV", "development")
    if file_config and "environments" in file_config and env in file_config["environments"]:
        env_config = file_config["environments"][env]
        for section, values in env_config.items():
            if section in config:
                config[section].update(values)
    
    # Override with environment variables
    if os.getenv("API_HOST"):
        config["api"]["host"] = os.getenv("API_HOST")
    if os.getenv("API_PORT"):
        config["api"]["port"] = int(os.getenv("API_PORT"))
    if os.getenv("API_DEBUG"):
        config["api"]["debug"] = os.getenv("API_DEBUG").lower() == "true"
    if os.getenv("API_WORKERS"):
        config["api"]["workers"] = int(os.getenv("API_WORKERS"))
    if os.getenv("MODEL_NAME"):
        config["model"]["name"] = os.getenv("MODEL_NAME")
    if os.getenv("MODEL_MAX_LENGTH"):
        config["model"]["max_length"] = int(os.getenv("MODEL_MAX_LENGTH"))
    if os.getenv("MODEL_MIN_LENGTH"):
        config["model"]["min_length"] = int(os.getenv("MODEL_MIN_LENGTH"))
    if os.getenv("DATABASE_URL"):
        config["database"]["url"] = os.getenv("DATABASE_URL")
    if os.getenv("LOG_LEVEL"):
        config["logging"]["level"] = os.getenv("LOG_LEVEL")
    if os.getenv("LOG_FILE"):
        config["logging"]["file"] = os.getenv("LOG_FILE")
    if os.getenv("SEC_USER_AGENT"):
        config["sec_edgar"]["user_agent"] = os.getenv("SEC_USER_AGENT")
    
    return config

# Global configuration object
config = load_config() 