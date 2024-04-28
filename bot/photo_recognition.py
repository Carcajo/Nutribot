import openai
from config import settings

openai.api_key = settings.OPENAI_API_KEY


async def recognize_food(image_file):
    response = openai.Image.create(
        file=image_file,
        prompt="Identify the food items in this image and provide their approximate weights or portions.",
        n=1,
        size="1024x1024",
    )
    image_analysis = response["data"][0]["text"]
    return image_analysis