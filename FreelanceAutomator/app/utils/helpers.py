import re
from datetime import datetime
from typing import Optional

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def extract_price_from_text(text: str) -> Optional[float]:
    price_pattern = r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)'
    match = re.search(price_pattern, text)
    if match:
        price_str = match.group(1).replace(',', '')
        return float(price_str)
    return None

def is_simple_task(title: str, description: str) -> bool:
    simple_keywords = [
        'review', 'comment', 'feedback', 'rating',
        'short', 'simple', 'quick', 'easy',
        'write a', 'leave a', 'post a'
    ]
    
    text = (title + ' ' + description).lower()
    return any(keyword in text for keyword in simple_keywords)

def format_datetime(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def truncate_text(text: str, max_length: int = 100) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'
