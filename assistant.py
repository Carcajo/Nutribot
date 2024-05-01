import os
from config import Settings
from client import AsyncOpenAIClient

settings = Settings()
openai_auth_key = os.environ.get("OPENAI_API_KEY", settings.OPENAI_API_KEY)


def load_advice_from_file(file_path):
    with open(file_path, "rb") as f:
        advice_bytes = f.read()
        try:
            advice_text = advice_bytes.decode("utf-8")
        except UnicodeDecodeError:
            advice_text = advice_bytes.decode("latin-1")
    return advice_text


advice_text = load_advice_from_file("advice.docx")


async def get_answer(query, user_id):
    metadata = {"user_id": user_id}
    prompt = f"Вопрос: {query}\n\nИсточник информации: {advice_text}\n\nОтвет:"
    async with AsyncOpenAIClient() as client:
        response = await client.create_completion(
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
            model="text-davinci-003",
            metadata=metadata,
        )
    answer = response["choices"][0]["text"].strip()
    return answer