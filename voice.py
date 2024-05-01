import aiohttp
from config import Settings

settings = Settings()


async def transcribe_audio_async(audio_file):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "multipart/form-data",
            },
            data={"model": "whisper-1", "file": audio_file},
        ) as response:
            result = await response.json()
            return result["text"]


async def generate_audio_async(text):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/audio/translations",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"model": "whisper-1", "text": text, "response_format": "audio/mpeg"},
        ) as response:
            audio_data = await response.read()
            return audio_data
