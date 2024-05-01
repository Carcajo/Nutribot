import os
import aiohttp
from config import Settings

settings = Settings()
openai_auth_key = os.environ.get("OPENAI_API_KEY", settings.OPENAI_API_KEY)


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
            headers={"Authorization": f"Bearer {openai_auth_key}"},
        ) as response:
            return await response.json()
