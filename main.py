import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from bot.config import settings
from bot.models import User
from bot.assistant import get_answer, save_target
from bot.voice import transcribe_audio, generate_audio
from bot.photo_recognition import recognize_food
from bot.amplitude import send_event
from bot.state import get_state, set_state
from bot.validator import validate_target


logging.basicConfig(level=logging.INFO)


bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    target = State()
    query = State()
    photo = State()



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот-помощник по питанию. Какова твоя цель?")
    await Form.target.set()
    send_event("bot_started", message.from_user.id)



@dp.message_handler(state=Form.target)
async def process_target(message: types.Message, state: FSMContext):
    target = message.text.lower()
    if validate_target(target):
        user = User(id=message.from_user.id, username=message.from_user.username, target=target)
        await user.save(session)
        await save_target(user, target)
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
    send_event("query_asked", user_id, {"query": query, "target": target})



@dp.message_handler(state=Form.query, content_types=types.ContentTypes.VOICE)
async def process_voice(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    voice = await message.voice.get_file()
    data = await state.get_data()
    target = data.get('target')
    transcribed_text = await transcribe_audio(voice.file)
    answer = await get_answer(transcribed_text, target)
    audio_file = await generate_audio(answer)
    await message.answer_voice(audio_file)
    send_event("voice_query_asked", user_id, {"query": transcribed_text, "target": target})



@dp.message_handler(state=Form.query, content_types=types.ContentTypes.PHOTO)
async def process_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = message.photo[-1]
    data = await state.get_data()
    target = data.get('target')
    photo_file = await photo.get_file()
    analysis = await recognize_food(photo_file)
    await message.answer(analysis)
    send_event("photo_analyzed", user_id, {"target": target, "analysis": analysis})



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)