import openai
from config import SETTINGS


client = openai.AsyncOpenAI(api_key=SETTINGS.OPENAI_API_KEY)


async def generate_speech(input_text):
    response = await client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=input_text
    )
    return response.read()

async def transcribe_audio(audio_file):
    audio_file.name = "audio.ogg"
    transcription = await client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )
    return transcription.text
