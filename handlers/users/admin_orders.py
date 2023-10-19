from aiogram import types
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.inline.admin_keyboards import admin_order_decision_filter, admin_order_cancel, admin_order_decision_def, \
    admin_order_accepted_def, admin_order_accepted_filter, admin_order_canceled_filter
from loader import dp, db_manager, bot


@dp.callback_query_handler(admin_order_decision_filter.filter(action="admin_order_accept"), chat_id=ADMINS)
async def admin_order_accept_handler(call: CallbackQuery, callback_data: dict):
    order_id = int(callback_data.get("order_id"))
    user_id = int(callback_data.get("user_id"))

    if db_manager.update_order_status(order_id, "ACCEPTED"):
        text = f"🆔: {order_id}\nUshbu ID raqamli buyurtma qabul qilindi ✅"
    else:
        text = "Buyurtma qabul qilish jarayonida xatolik yuz berdi xo'jayin ❗️"

    await call.answer(text=text, show_alert=True)
    await bot.send_message(chat_id=user_id, text=text)


@dp.callback_query_handler(admin_order_cancel.filter(action="admin_order_cancel"), chat_id=ADMINS)
async def admin_order_accept_handler(call: CallbackQuery, callback_data: dict):
    order_id = int(callback_data.get("order_id"))
    user_id = int(callback_data.get("user_id"))

    if db_manager.update_order_status(order_id, "CANCELED"):
        text = f"🆔: {order_id}\nUshbu ID raqamli buyurtma qabul qilinmadi ❌"
    else:
        text = "Buyurtma qabul qilish jarayonida xatolik yuz berdi xo'jayin ❗️"

    await bot.send_message(chat_id=user_id, text=text)
    await call.answer(text=text, show_alert=True)


@dp.callback_query_handler(admin_order_accepted_filter.filter(action="admin_order_delivered"), chat_id=ADMINS)
async def admin_order_delivered_handler(call: CallbackQuery, callback_data: dict):
    order_id = int(callback_data.get("order_id"))

    if db_manager.update_order_status(order_id, "DELIVERED"):
        text = f"🆔: {order_id}\nUshbu ID raqamli buyurtma yetkazib berildi ✅"
    else:
        text = "Buyurtma qabul qilish jarayonida xatolik yuz berdi xo'jayin ❗️"

    await call.answer(text=text, show_alert=True)


@dp.callback_query_handler(admin_order_canceled_filter.filter(action="admin_order_canceled"), chat_id=ADMINS)
async def admin_order_canceled_handler(call: CallbackQuery, callback_data: dict):
    order_id = int(callback_data.get("order_id"))

    if db_manager.update_order_status(order_id, "DELETED"):
        text = "Buyurtma o'chirildi ✅"
    else:
        text = "Buyurtmani o'chirish jarayonida xatolik yuz berdi xo'jayin ❗️"

    await call.answer(text=text, show_alert=True)