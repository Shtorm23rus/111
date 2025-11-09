from app.ai.base_generator import BaseContentGenerator
from app.ai.prompt_templates import reviews, comments, posts
from app.utils.logger import get_logger
from typing import Optional, List

logger = get_logger(__name__)

class ReviewGenerator(BaseContentGenerator):
    def generate(
        self,
        job_description: str,
        requirements: Optional[str] = None,
        tone: str = "positive",
        **kwargs
    ) -> str:
        logger.info("Generating review")
        
        system_prompt = reviews.REVIEW_SYSTEM_PROMPT
        user_prompt = reviews.get_review_prompt(job_description, requirements, tone)
        
        generated_review = self.client.generate_text(
            prompt=user_prompt,
            system_prompt=system_prompt,
            **kwargs
        )
        
        return self._clean_generated_content(generated_review)
    
    def generate_product_review(
        self,
        product_name: str,
        rating: int,
        key_points: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        logger.info(f"Generating product review for: {product_name}")
        
        system_prompt = reviews.REVIEW_SYSTEM_PROMPT
        user_prompt = reviews.get_product_review_prompt(product_name, rating, key_points)
        
        generated_review = self.client.generate_text(
            prompt=user_prompt,
            system_prompt=system_prompt,
            **kwargs
        )
        
        return self._clean_generated_content(generated_review)

class CommentGenerator(BaseContentGenerator):
    def generate(
        self,
        topic: str,
        context: Optional[str] = None,
        length: str = "medium",
        **kwargs
    ) -> str:
        logger.info(f"Generating comment on topic: {topic}")
        
        system_prompt = comments.COMMENT_SYSTEM_PROMPT
        user_prompt = comments.get_comment_prompt(topic, context, length)
        
        generated_comment = self.client.generate_text(
            prompt=user_prompt,
            system_prompt=system_prompt,
            **kwargs
        )
        
        return self._clean_generated_content(generated_comment)

class PostGenerator(BaseContentGenerator):
    def generate(
        self,
        topic: str,
        platform: str = "generic",
        target_audience: Optional[str] = None,
        **kwargs
    ) -> str:
        logger.info(f"Generating post for platform: {platform}")
        
        system_prompt = posts.POST_SYSTEM_PROMPT
        user_prompt = posts.get_post_prompt(topic, platform, target_audience)
        
        generated_post = self.client.generate_text(
            prompt=user_prompt,
            system_prompt=system_prompt,
            **kwargs
        )
        
        return self._clean_generated_content(generated_post)

class ContentGeneratorFactory:
    @staticmethod
    def get_generator(content_type: str) -> BaseContentGenerator:
        generators = {
            'review': ReviewGenerator,
            'comment': CommentGenerator,
            'post': PostGenerator,
            'feedback': ReviewGenerator,
        }
        
        generator_class = generators.get(content_type.lower())
        if not generator_class:
            raise ValueError(f"Unknown content type: {content_type}")
        
        return generator_class()
