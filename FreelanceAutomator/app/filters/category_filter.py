from typing import List, Dict, Any
from app.filters.base_filter import BaseFilter
from app.utils.logger import get_logger

logger = get_logger(__name__)

class CategoryFilter(BaseFilter):
    def __init__(self, allowed_categories: List[str]):
        self.allowed_categories = [cat.lower() for cat in allowed_categories]
    
    def filter(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered = [
            job for job in jobs
            if job.get('category', '').lower() in self.allowed_categories
        ]
        
        logger.info(f"CategoryFilter: {len(jobs)} -> {len(filtered)} jobs")
        return filtered
