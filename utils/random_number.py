import random

from aiogram import Bot

from loader import db_manager


def get_random_id():
    try:
        random_num = random.randint(10000, 99999)
        order = db_manager.get_order_by_id(random_num)
        if order:
            if order[3] == "DELIVERED" or order[3] == "CANCELED":
                return random_num
            else:
                get_random_id()
        return random_num
    except Exception as exc:
        print(exc)
        return 00000


async def check_user_membership(chat_id: int, channel_id: int):
    try:
        bot = Bot.get_current()
        member = await bot.get_chat_member(chat_id=channel_id, user_id=chat_id)
        return member.is_chat_member()
    except Exception as exc:
        print(exc)
        return False
