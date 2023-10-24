from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        chat_id = message.chat.id
        if str(chat_id) in ADMINS:
            return True
        return False
