import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from middlewares.database import DatabaseSessionMiddleware
from config import SETTINGS
import private_messages


async def start(session)-> None:
    bot = Bot(token=SETTINGS.BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.message.middleware(DatabaseSessionMiddleware(session))

    dp.include_router(private_messages.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    engine = create_async_engine(SETTINGS.DATABASE_URL_ASYNC, echo=True)
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start(Session))
