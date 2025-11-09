import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('logs/app.log', maxBytes=10485760, backupCount=5),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info('Logger initialized successfully')
    return logger

def get_logger(name):
    return logging.getLogger(name)
