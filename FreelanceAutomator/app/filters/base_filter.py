from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseFilter(ABC):
    @abstractmethod
    def filter(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass
    
    def __call__(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self.filter(jobs)
