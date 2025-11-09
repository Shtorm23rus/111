from typing import List, Dict, Any
from app.filters.base_filter import BaseFilter
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ComplexityFilter(BaseFilter):
    def __init__(self, max_complexity: int = 2):
        self.max_complexity = max_complexity
    
    def filter(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered = [
            job for job in jobs
            if job.get('complexity', 1) <= self.max_complexity
        ]
        
        logger.info(f"ComplexityFilter: {len(jobs)} -> {len(filtered)} jobs")
        return filtered
