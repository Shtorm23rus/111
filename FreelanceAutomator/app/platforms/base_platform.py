from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.utils.logger import get_logger

logger = get_logger(__name__)

class BasePlatform(ABC):
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        logger.info(f"Initialized {platform_name} platform")
    
    @abstractmethod
    def fetch_jobs(self, **kwargs) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def parse_job(self, job_data: Any) -> Dict[str, Any]:
        pass
