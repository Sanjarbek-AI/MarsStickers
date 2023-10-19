from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.admin_menu import admin_main_menu
from keyboards.inline.admin_keyboards import *
from loader import dp, db_manager
from states.admins import StickerUpdateState


@dp.callback_query_handler(admin_sticker_change_photo.filter(action="change_sticker_photo"), state="admin-stickers-state")
async def admin_change_photo_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    sticker_id = callback_data.get('sticker_id')
    await state.update_data(sticker_id=sticker_id)
    text = "Yangi rasmni kiriting."
    await call.message.answer(text=text)
    await StickerUpdateState.photo.set()


@dp.message_handler(state=StickerUpdateState.photo, content_types=types.ContentType.PHOTO)
async def update_photo_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sticker_id = data.get('sticker_id')
    photo = message.photo[-1].file_id

    if db_manager.update_admin_sticker(sticker_id, "photo", photo):
        text = "Rasm yangilandi."
    else:
        text = "Xatolik bor."
    await message.answer(text=text, reply_markup=admin_main_menu)
    await state.finish()
