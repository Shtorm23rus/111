REVIEW_SYSTEM_PROMPT = """Вы - эксперт по написанию естественных и убедительных отзывов на различные продукты и услуги. 
Ваша задача - создавать отзывы, которые звучат естественно и человечно, избегая клише и шаблонных фраз.
Отзывы должны быть:
- Конкретными и детальными
- Сбалансированными (могут содержать как положительные, так и нейтральные моменты)
- Написанными простым, разговорным языком
- Уникальными и не похожими на автоматически сгенерированный текст
"""

def get_review_prompt(job_description: str, requirements: str = None, tone: str = "positive") -> str:
    base_prompt = f"""Задание: {job_description}

Требования к отзыву:
- Тон: {tone}
- Длина: 100-300 слов
- Стиль: естественный, человечный"""
    
    if requirements:
        base_prompt += f"\n- Дополнительные требования: {requirements}"
    
    base_prompt += "\n\nНапишите отзыв, который полностью соответствует заданию."
    
    return base_prompt

def get_product_review_prompt(product_name: str, rating: int, key_points: list = None) -> str:
    prompt = f"""Напишите отзыв о продукте: {product_name}
Оценка: {rating}/5 звезд

"""
    
    if key_points:
        prompt += "Упомяните следующие моменты:\n"
        for point in key_points:
            prompt += f"- {point}\n"
    
    prompt += "\nОтзыв должен быть естественным и убедительным."
    
    return prompt
