import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///freelance_assistant.db')
    
    UPWORK_CLIENT_ID = os.getenv('UPWORK_CLIENT_ID', '')
    UPWORK_CLIENT_SECRET = os.getenv('UPWORK_CLIENT_SECRET', '')
    UPWORK_ACCESS_TOKEN = os.getenv('UPWORK_ACCESS_TOKEN', '')
    
    SCHEDULER_INTERVAL_MINUTES = int(os.getenv('SCHEDULER_INTERVAL_MINUTES', 30))
    
    MIN_JOB_PRICE = float(os.getenv('MIN_JOB_PRICE', 10))
    MAX_JOB_PRICE = float(os.getenv('MAX_JOB_PRICE', 500))
    TARGET_CATEGORIES = os.getenv('TARGET_CATEGORIES', 'review,comment,feedback,writing').split(',')
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
