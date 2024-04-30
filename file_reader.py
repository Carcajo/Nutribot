import openai
from config import Settings

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY


def load_advice_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        advice_text = f.read()
    return advice_text


advice_text = load_advice_from_file("advice.docx")
