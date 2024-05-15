import base64
import openai
from config import SETTINGS


client = openai.AsyncOpenAI(api_key=SETTINGS.OPENAI_API_KEY)

PROMT = """\
Определите продукты питания на этом изображении и укажите их приблизительный вес или порции. В ответе укажите только количество граммов и калорий. Пиши только название, вес: количество грамм и энергетическую ценность: количество ккал.
"""

async def recognize_food(image_bytes):
    image_base64 = "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode('utf-8')
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_base64,
                        },
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content
