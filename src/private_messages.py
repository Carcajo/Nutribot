from aiogram import F, Router, Bot
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InputFile, Message, ContentType
from sqlalchemy.ext.asyncio import AsyncSession

from ai.photo_recognition import recognize_food
from ai.voice_tools import generate_speech, transcribe_audio
import amplitude_events
import bot_responses
import io

from aiogram_filters import ChatTypeFilter, ContentTypeFilter
from model.user import User
from ai.process_text_message import process_text_message

router = Router()
router.message.filter(ChatTypeFilter([ChatType.PRIVATE]))


@router.message(CommandStart())
async def command_start_handler(message: Message, session: AsyncSession) -> None:
    await message.answer(bot_responses.START_RESPONSE)
    if message.from_user is None:
        return

    user_id = message.from_user.id
    if await User.user_exists_by_id(session, user_id):
        pass
    else:
        session.add(User(id=message.from_user.id))
        await session.commit()


@router.message(F.text)
async def text_message(message: Message, session: AsyncSession, bot: Bot) -> None:
    amplitude_events.user_text_message(message.from_user.id, message.text)
    wait_message = await message.reply("Подождите...")
    await bot.send_chat_action(message.chat.id, 'typing')

    user = await User.get_user_by_id(session, message.from_user.id)
    response = await process_user_message(message.text, user, session)
    await wait_message.edit_text(response)


@router.message(F.photo)
async def process_photo(message: Message, bot: Bot):
    amplitude_events.user_photo_message(message.from_user.id)
    wait_message = await message.reply("Подождите...")
    await bot.send_chat_action(message.chat.id, 'typing')
    assert message.from_user is not None
    assert message.photo is not None
    photo = message.photo[-1]

    photo_file = io.BytesIO()
    file = await bot.get_file(photo.file_id)
    await bot.download(file, photo_file)
    response = await recognize_food(photo_file.read())
    await wait_message.edit_text(response or r"¯\_(ツ)_/¯")
    #send_event_async("photo_analyzed", user_id, {"target": target, "analysis": analysis})


@router.message(ContentTypeFilter(ContentType.VOICE))
async def process_voice_message(message: Message, bot: Bot, session: AsyncSession):
    await bot.send_chat_action(message.chat.id, 'record_voice')
    assert message.voice is not None
    assert message.from_user is not None

    user = await User.get_user_by_id(session, message.from_user.id)
    assert user is not None

    file = await bot.get_file(message.voice.file_id)
    voice_file = io.BytesIO()
    await bot.download(file, voice_file)
    user_request = await transcribe_audio(voice_file)

    amplitude_events.user_voice_message(message.from_user.id, user_request)

    await bot.send_chat_action(message.chat.id, 'typing')
    ai_response = await process_user_message(user_request, user, session)
    audio_tts = await generate_speech(ai_response)
    await message.answer_voice(BufferedInputFile(audio_tts, "response.mp3"))


async def process_user_message(message_text: str, user: User, session: AsyncSession) -> str:
    response = await process_text_message(user.openai_thread_id, message_text, user.goal)
    user.openai_thread_id = response.openai_thread_id
    user.goal = response.goal
    await session.commit()
    return response.response
