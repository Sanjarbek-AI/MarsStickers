from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS, CHANNELS
from keyboards.default.admin_menu import admin_main_menu
from keyboards.default.little import phone_number_share
from keyboards.default.user_menu import user_main_menu
from keyboards.inline.user_keyboards import channels_keyboards
from loader import dp, db_manager
from states.users import Register
from test import login
from utils.random_number import check_user_membership


@dp.message_handler(commands="start", chat_id=ADMINS)
async def admin_start_handler(message: types.Message):
    text = "Botga xush kelibsiz xo'jayin. 😊"
    await message.answer(text=text, reply_markup=admin_main_menu)


@dp.message_handler(commands="start", state="*")
async def start_handler(message: types.Message, state: FSMContext):
    check = True
    not_member = []
    for channel in CHANNELS:
        if await check_user_membership(chat_id=message.chat.id, channel_id=channel['id']):
            pass
        else:
            not_member.append(channel)
            check = False

    if check:
        if db_manager.get_user(message):
            text = "Botga xush kelibsiz. 😊"
            await message.answer(text=text, reply_markup=user_main_menu)
            await state.finish()
        else:
            text = "Iltimos to'liq ismingizni kiriting."
            await message.answer(text=text)
            await Register.full_name.set()
    else:
        text = "Botni ishga tushirish uchun, ushbu kanllarga a'zo bo'ling"
        await message.answer(text=text, reply_markup=await channels_keyboards(not_member))


@dp.message_handler(state=Register.full_name)
async def full_name_state(message: types.Message, state: FSMContext):
    await state.update_data({
        "full_name": message.text
    })

    text = "Iltimos telefon raqamingizni kiriting."
    await message.answer(text=text, reply_markup=phone_number_share)
    await Register.phone_number.set()


@dp.message_handler(state=Register.phone_number, content_types=types.ContentType.CONTACT)
async def phone_number_state(message: types.Message, state: FSMContext):
    await state.update_data({
        "phone_number": message.contact.phone_number
    })

    text = "Iltimos modme id ni kiriting."
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await Register.modme_id.set()


@dp.message_handler(state=Register.modme_id)
async def modme_id_state(message: types.Message, state: FSMContext):
    await state.update_data({
        "modme_id": message.text
    })

    text = "Iltimos parolni kiriting."
    await message.answer(text=text)
    await Register.parol.set()


@dp.message_handler(state=Register.parol)
async def parol_state(message: types.Message, state: FSMContext):
    await state.update_data({
        "parol": message.text
    })

    text = "Iltimos guruh raqamni kiriting."
    await message.answer(text=text)
    await Register.group_number.set()


@dp.message_handler(state=Register.group_number)
async def group_number_state(message: types.Message, state: FSMContext):
    await state.update_data({
        "group_number": message.text
    })

    text = "Iltimos, qaysi kursda o'qishingizni kiriting."
    await message.answer(text=text)
    await Register.group_type.set()


@dp.message_handler(state=Register.group_type)
async def group_type_state(message: types.Message, state: FSMContext):
    await state.update_data({
        "group_type": message.text,
        "user_id": message.chat.id,
    })
    data = await state.get_data()
    modme_id = data.get("modme_id")
    parol = data.get("parol")
    token = login(modme_id, parol)

    if token:
        await state.update_data({
            "token": token
        })
        data = await state.get_data()
        if db_manager.append_user(data):
            text = "Siz muvofaqqiyatli ro'yxatdan o'tdingiz. ✅"
        else:
            text = "Botda muommo mavjud, biz bilan bog'laning"
        await message.answer(text=text, reply_markup=user_main_menu)
    else:
        text = "Siz MARS IT SCHOOL o'quvchisi emassiz, yoki siz kiritgan ma'lumotlar noto'g'ri"
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.finish()
