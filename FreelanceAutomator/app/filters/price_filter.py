from typing import List, Dict, Any, Optional
from app.filters.base_filter import BaseFilter
from app.utils.logger import get_logger

logger = get_logger(__name__)

class PriceFilter(BaseFilter):
    def __init__(self, min_price: Optional[float] = None, max_price: Optional[float] = None):
        self.min_price = min_price
        self.max_price = max_price
    
    def filter(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered = []
        
        for job in jobs:
            budget = job.get('budget')
            
            if budget is None:
                filtered.append(job)
                continue
            
            if self.min_price and budget < self.min_price:
                continue
            
            if self.max_price and budget > self.max_price:
                continue
            
            filtered.append(job)
        
        logger.info(f"PriceFilter: {len(jobs)} -> {len(filtered)} jobs")
        return filtered
