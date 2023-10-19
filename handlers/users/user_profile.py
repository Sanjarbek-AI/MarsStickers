from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.user_menu import user_main_menu, user_main_menu_back
from keyboards.inline.user_keyboards import user_profile_menu
from loader import dp, db_manager
from states.users import ProfileUpdate


@dp.message_handler(text="👤 Profile")
async def profile_menu_handler(message: types.Message):
    user = db_manager.get_user(message)
    if user:
        text = f"""
FI: {user[2]}
TEL: {user[3]}
ID: {user[4]}
Guruh raqam: {user[5]}
Guruh turi: {user[6]}
"""
        await message.answer(text=text, reply_markup=user_profile_menu)
    else:
        text = "Siz haqingizda ma'lumot topilmadi."
        await message.answer(text=text)


@dp.callback_query_handler(text="change_full_name")
async def change_full_name_handler(call: CallbackQuery):
    text = "Yangi ismni kiriting."
    await call.message.answer(text=text, reply_markup=user_main_menu_back)
    await ProfileUpdate.full_name.set()


@dp.message_handler(state=ProfileUpdate.full_name)
async def update_user_full_name(message: types.Message, state: FSMContext):
    if db_manager.update_user_profile(message, "full_name"):
        text = "Yangilandi."
    else:
        text = "Xatolik bor"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()
