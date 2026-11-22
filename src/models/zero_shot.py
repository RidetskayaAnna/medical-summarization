import time
import os
from models.model_loader import get_llm_client

client = get_llm_client()

def get_zero_shot_summary(text, max_retries=5):
    # Читаем промпт из файла
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "zero_shot_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()
        
    prompt = prompt_template.format(text=text)

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "429" in str(e) or "Too many requests" in str(e):
                time.sleep((attempt + 1) * 10)
            else:
                print(f"Ошибка API (Zero-shot): {e}")
                return "ОШИБКА"
    return "ОШИБКА"