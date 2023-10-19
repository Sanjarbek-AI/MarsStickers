from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

admin_order_decision_filter = CallbackData("admin_order_accept", "action", "order_id", "user_id")
admin_order_cancel = CallbackData("admin_order_cancel", "action", "order_id", "user_id")

admin_order_accepted_filter = CallbackData("admin_order_delivered", "action", "order_id", "user_id")
admin_order_canceled_filter = CallbackData("admin_order_canceled", "action", "order_id", "user_id")

admin_sticker_change_photo = CallbackData("change_sticker_photo", "action", "sticker_id")
admin_sticker_change_price = CallbackData("change_sticker_price", "action", "sticker_id")
admin_sticker_change_name = CallbackData("change_sticker_name", "action", "sticker_id")
admin_sticker_change_quantity = CallbackData("change_sticker_quantity ", "action", "sticker_id")
admin_sticker_change_description = CallbackData("change_sticker_description", "action", "sticker_id")
admin_sticker_delete = CallbackData("change_sticker_delete", "action", "sticker_id")


async def admin_order_decision_def(order_id: int, user_id: int):
    admin_order_decision = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Qabul qilish",
                    callback_data=admin_order_decision_filter.new(action="admin_order_accept", order_id=order_id,
                                                                  user_id=user_id)),

                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data=admin_order_cancel.new(action="admin_order_cancel", order_id=order_id,
                                                         user_id=user_id))
            ]
        ]
    )
    return admin_order_decision


async def admin_order_accepted_def(order_id: int, user_id: int):
    admin_order_accepted = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Yetkazib berildi",
                    callback_data=admin_order_accepted_filter.new(action="admin_order_delivered", order_id=order_id,
                                                                  user_id=user_id)),

                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data=admin_order_cancel.new(action="admin_order_cancel", order_id=order_id,
                                                         user_id=user_id))
            ]
        ]
    )
    return admin_order_accepted


async def admin_order_canceled_def(order_id: int, user_id: int):
    admin_order_canceled = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 O'chirib tashlash",
                    callback_data=admin_order_canceled_filter.new(action="admin_order_canceled", order_id=order_id,
                                                                  user_id=user_id))
            ]
        ]
    )
    return admin_order_canceled


async def admin_order_search_def(order_id: int, user_id: int):
    admin_order_search = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Qabul qilish",
                    callback_data=admin_order_decision_filter.new(action="admin_order_accept", order_id=order_id,
                                                                  user_id=user_id))
            ],
            [

                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data=admin_order_cancel.new(action="admin_order_cancel", order_id=order_id,
                                                         user_id=user_id))
            ],
            [
                InlineKeyboardButton(
                    text="🗑 O'chirib tashlash",
                    callback_data=admin_order_canceled_filter.new(action="admin_order_canceled", order_id=order_id,
                                                                  user_id=user_id))
            ],
            [
                InlineKeyboardButton(
                    text="✅ Yetkazib berildi",
                    callback_data=admin_order_accepted_filter.new(action="admin_order_delivered", order_id=order_id,
                                                                  user_id=user_id))
            ]
        ]
    )
    return admin_order_search


async def admin_sticker_change_def(sticker_id: int):
    admin_sticker_change = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Rasm",
                    callback_data=admin_sticker_change_photo.new(action="change_sticker_photo", sticker_id=sticker_id)),
                InlineKeyboardButton(
                    text="Nomi",
                    callback_data=admin_sticker_change_name.new(action="change_sticker_name", sticker_id=sticker_id))
            ],
            [
                InlineKeyboardButton(
                    text="Narxi",
                    callback_data=admin_sticker_change_price.new(action="change_sticker_price", sticker_id=sticker_id)),
                InlineKeyboardButton(
                    text="Ma'lumot",
                    callback_data=admin_sticker_change_description.new(action="change_sticker_description",
                                                                       sticker_id=sticker_id))
            ],
            [
                InlineKeyboardButton(
                    text="Soni",
                    callback_data=admin_sticker_change_quantity.new(action="change_sticker_quantity",
                                                                    sticker_id=sticker_id)),
                InlineKeyboardButton(
                    text="O'chirish",
                    callback_data=admin_sticker_delete.new(action="change_sticker_delete",
                                                           sticker_id=sticker_id))
            ],
        ]
    )
    return admin_sticker_change
