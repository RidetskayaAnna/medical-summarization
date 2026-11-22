import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_llm_client():
    """Возвращает инициализированный клиент для работы с API."""
    return OpenAI(
        api_key=os.getenv("AIAI_API_KEY"),
        base_url="https://api.aiai.by/v1"
    )