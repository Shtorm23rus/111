from app.ai.anthropic_client import AnthropicClient
from app.utils.logger import get_logger
from typing import Optional, Dict

logger = get_logger(__name__)

class ProposalGenerator:
    def __init__(self):
        self.client = AnthropicClient()
    
    def generate_proposal(
        self,
        job_title: str,
        job_description: str,
        freelancer_profile: Optional[Dict] = None,
        budget: Optional[float] = None,
        **kwargs
    ) -> str:
        logger.info(f"Generating proposal for job: {job_title}")
        
        system_prompt = self._get_system_prompt()
        user_prompt = self._build_user_prompt(
            job_title,
            job_description,
            freelancer_profile,
            budget
        )
        
        try:
            proposal = self.client.generate_text(
                prompt=user_prompt,
                system_prompt=system_prompt,
                max_tokens=1500,
                temperature=0.7,
                **kwargs
            )
            
            return self._clean_proposal(proposal)
        except Exception as e:
            logger.error(f"Error generating proposal: {e}")
            raise
    
    def generate_short_proposal(
        self,
        job_title: str,
        job_description: str,
        **kwargs
    ) -> str:
        logger.info(f"Generating short proposal for: {job_title}")
        
        system_prompt = """Ты профессиональный фрилансер, который пишет короткие и эффективные предложения для заказов.
        Твоя задача - создать краткое, но убедительное предложение (cover letter) объемом 2-3 предложения."""
        
        user_prompt = f"""Задание: {job_title}

Описание: {job_description}

Напиши короткое предложение (2-3 предложения), которое:
1. Подчеркивает твою квалификацию для этого задания
2. Показывает понимание требований
3. Выражает готовность начать работу

Напиши только текст предложения, без дополнительных комментариев."""
        
        try:
            proposal = self.client.generate_text(
                prompt=user_prompt,
                system_prompt=system_prompt,
                max_tokens=300,
                temperature=0.6,
                **kwargs
            )
            
            return self._clean_proposal(proposal)
        except Exception as e:
            logger.error(f"Error generating short proposal: {e}")
            raise
    
    def _get_system_prompt(self) -> str:
        return """Ты опытный фрилансер с многолетним стажем работы на международных платформах.
        Твоя специализация - написание качественного контента, отзывов, комментариев и статей.
        
        При написании предложений (proposals/cover letters) ты:
        1. Демонстрируешь понимание задачи и требований клиента
        2. Подчеркиваешь релевантный опыт и навыки
        3. Используешь профессиональный, но дружелюбный тон
        4. Предлагаешь конкретные решения и подходы
        5. Избегаешь шаблонных фраз и общих мест
        6. Пишешь кратко и по существу
        
        Всегда пиши на языке описания задания (английский или русский)."""
    
    def _build_user_prompt(
        self,
        job_title: str,
        job_description: str,
        freelancer_profile: Optional[Dict],
        budget: Optional[float]
    ) -> str:
        prompt = f"""Напиши профессиональное предложение (cover letter) для следующего задания:

ЗАДАНИЕ: {job_title}

ОПИСАНИЕ ЗАДАНИЯ:
{job_description}
"""
        
        if budget:
            prompt += f"\nБЮДЖЕТ: ${budget}\n"
        
        if freelancer_profile:
            prompt += "\nПРОФИЛЬ ФРИЛАНСЕРА:\n"
            if 'name' in freelancer_profile:
                prompt += f"Имя: {freelancer_profile['name']}\n"
            if 'skills' in freelancer_profile:
                prompt += f"Навыки: {', '.join(freelancer_profile['skills'])}\n"
            if 'experience' in freelancer_profile:
                prompt += f"Опыт: {freelancer_profile['experience']}\n"
        
        prompt += """
Напиши предложение, которое:
1. Обращается к клиенту и показывает понимание его потребностей
2. Подчеркивает релевантный опыт и навыки для выполнения этого задания
3. Предлагает конкретный подход к выполнению работы
4. Выражает готовность обсудить детали и ответить на вопросы
5. Имеет профессиональный, но дружелюбный тон
6. Состоит из 4-6 коротких абзацев

Напиши только текст предложения, без дополнительных комментариев или объяснений."""
        
        return prompt
    
    def _clean_proposal(self, proposal: str) -> str:
        proposal = proposal.strip()
        
        unwanted_phrases = [
            "Here is a proposal",
            "Here's a proposal",
            "Вот предложение",
            "Dear Client,",
            "Уважаемый клиент,",
        ]
        
        for phrase in unwanted_phrases:
            if proposal.startswith(phrase):
                proposal = proposal[len(phrase):].strip()
        
        lines = [line.strip() for line in proposal.split('\n') if line.strip()]
        proposal = '\n\n'.join(lines)
        
        return proposal
