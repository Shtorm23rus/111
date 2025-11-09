from anthropic import Anthropic
from app.core.config import Config
from app.core.exceptions import AIGenerationError, ConfigurationError
from app.utils.logger import get_logger
from typing import Optional

logger = get_logger(__name__)

class AnthropicClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        
        if not self.api_key:
            raise ConfigurationError("ANTHROPIC_API_KEY not provided")
        
        try:
            self.client = Anthropic(api_key=self.api_key)
            logger.info("Anthropic client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            raise ConfigurationError(f"Failed to initialize Anthropic client: {e}")
    
    def generate_text(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> str:
        try:
            logger.info(f"Generating text with model: {model}")
            
            kwargs = {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            if system_prompt:
                kwargs["system"] = system_prompt
            
            message = self.client.messages.create(**kwargs)
            
            if not message.content:
                raise AIGenerationError("Empty response from AI")
            
            text_content = next((block.text for block in message.content if hasattr(block, 'text')), None)
            if not text_content:
                raise AIGenerationError("No text content in response")
            
            logger.info(f"Successfully generated text ({len(text_content)} chars)")
            
            return text_content
            
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise AIGenerationError(f"Failed to generate text: {e}")
    
    def generate_with_retry(
        self,
        prompt: str,
        system_prompt: str = "",
        max_retries: int = 3,
        **kwargs
    ) -> str:
        last_error = None
        
        for attempt in range(max_retries):
            try:
                return self.generate_text(prompt, system_prompt, **kwargs)
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    continue
        
        raise AIGenerationError(f"Failed after {max_retries} attempts: {last_error}")
