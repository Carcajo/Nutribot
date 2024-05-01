import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import Settings
from models import User, get_db_pool
from assistant import get_answer
from voice import transcribe_audio_async, generate_audio_async
from photo_recognition import recognize_food
from amplit import send_event_async
from validator import validate_target

settings = Settings()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.BOT_TOKEN)
storage = RedisStorage2(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
dp = Dispatcher(bot, storage=storage)

async def get_session() -> AsyncSession:
    async with get_db_pool() as pool:
        async_session = sessionmaker(
            pool, class_=AsyncSession, expire_on_commit=False
        )
        yield async_session


class Form(StatesGroup):
    target = State()
    query = State()
    photo = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот-помощник по питанию. Какова твоя цель?")
    await Form.target.set()
    send_event_async("bot_started", message.from_user.id)


@dp.message_handler(state=Form.target)
async def process_target(message: types.Message, state: FSMContext):
    target = message.text.lower()
    if validate_target(target):
        async_session = await get_session()
        async with async_session() as session:
            user = User(id=message.from_user.id, username=message.from_user.username, target=target)
            await user.save(session)
        await state.update_data(target=target)
        await message.answer(f"Отлично, твоя цель: {target}. Задавай свой вопрос!")
        await Form.query.set()
    else:
        await message.answer("Извини, я не понял твою цель. Попробуй еще раз.")


@dp.message_handler(state=Form.query, content_types=types.ContentTypes.TEXT)
async def process_query(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    target = data.get('target')
    query = message.text
    answer = await get_answer(query, target)
    await message.answer(answer)
    send_event_async("query_asked", user_id, {"query": query, "target": target})


@dp.message_handler(state=Form.query, content_types=types.ContentTypes.VOICE)
async def process_voice(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    voice = await message.voice.get_file()
    data = await state.get_data()
    target = data.get('target')
    transcribed_text = await transcribe_audio_async(voice.file)
    answer = await get_answer(transcribed_text, target)
    audio_file = await generate_audio_async(answer)
    await message.answer_voice(audio_file)
    send_event_async("voice_query_asked", user_id, {"query": transcribed_text, "target": target})


@dp.message_handler(state=Form.query, content_types=types.ContentTypes.PHOTO)
async def process_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = message.photo[-1]
    data = await state.get_data()
    target = data.get('target')
    photo_file = await photo.get_file()
    analysis = await recognize_food(photo_file)
    await message.answer(analysis)
    send_event_async("photo_analyzed", user_id, {"target": target, "analysis": analysis})


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
