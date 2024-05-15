from aiogram.filters import Filter
from aiogram import types


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class ContentTypeFilter(Filter):
    def __init__(self, content_type: str) -> None:
        self.content_type = content_type

    async def __call__(self, message: types.Message) -> bool:
        return message.content_type == self.content_type
