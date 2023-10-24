from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNELS
from keyboards.inline.user_keyboards import channels_keyboards
from utils.random_number import check_user_membership


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            message = update.message
            user_id = message.chat.id
        elif update.callback_query:
            message = update.callback_query.message
            user_id = message.chat.id
        else:
            return

        check = True
        not_member = []
        for channel in CHANNELS:
            if not await check_user_membership(chat_id=user_id, channel_id=channel['id']):
                not_member.append(channel)
                check = False
        if check is False:
            text = "Botni ishga tushirish uchun, ushbu kanllarga a'zo bo'ling"
            await message.answer(text, disable_web_page_preview=True,
                                 reply_markup=await channels_keyboards(not_member))
            raise CancelHandler()
