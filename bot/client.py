import openai
import aiohttp
from config import settings

openai.api_key = settings.OPENAI_API_KEY


class AsyncOpenAIClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def create_completion(self, **kwargs):
        async with self.session.post(
            "https://api.openai.com/v1/completions",
            json=kwargs,
        ) as response:
            return await response.json()
