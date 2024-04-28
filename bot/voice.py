import openai
from config import settings

openai.api_key = settings.OPENAI_API_KEY


async def transcribe_audio(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text


async def generate_audio(text):
    audio = openai.Audio.create_audio(
        text=text,
        model="whisper-1",
        response_format="audio/mpeg",
    )
    return audio.data