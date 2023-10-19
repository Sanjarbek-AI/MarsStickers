from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.admin_menu import admin_main_menu
from keyboards.default.user_menu import user_main_menu
from loader import dp


@dp.message_handler(text="⬅️ Back", state="*")
async def stickers_menu(message: types.Message, state: FSMContext):
    text = "Welcom to main menu"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()


@dp.message_handler(text="Back ⬅️", chat_id=ADMINS, state="*")
async def stickers_menu(message: types.Message, state: FSMContext):
    text = "Welcom to main menu"
    await message.answer(text=text, reply_markup=admin_main_menu)
    await state.finish()
