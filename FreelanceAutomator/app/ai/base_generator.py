from abc import ABC, abstractmethod
from typing import Dict, Any
from app.ai.anthropic_client import AnthropicClient
from app.utils.logger import get_logger

logger = get_logger(__name__)

class BaseContentGenerator(ABC):
    def __init__(self, anthropic_client: AnthropicClient = None):
        self.client = anthropic_client or AnthropicClient()
    
    @abstractmethod
    def generate(self, **kwargs) -> str:
        pass
    
    def _clean_generated_content(self, content: str) -> str:
        content = content.strip()
        return content
