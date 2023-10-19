from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.admin_menu import admin_stickers_menu_def, admin_back_main_menu
from keyboards.inline.admin_keyboards import admin_sticker_change_def
from loader import dp, db_manager
from states.admins import StickerState


@dp.message_handler(text="Stickers 💥", chat_id=ADMINS)
async def admin_order_handler(message: types.Message, state: FSMContext):
    await state.set_state('admin-stickers-state')
    text = "Mahsulotlar manyusiga xush kelibsiz"
    await message.answer(text=text, reply_markup=await admin_stickers_menu_def())


@dp.message_handler(text="Sticker qo'shish ➕", chat_id=ADMINS)
async def add_sticker_handler(message: types.Message):
    text = "Mahsulot nomini kiriting."
    await message.answer(text=text, reply_markup=admin_back_main_menu)
    await StickerState.name.set()


@dp.message_handler(state=StickerState.name, chat_id=ADMINS)
async def get_sticker_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "name": message.text
    })
    text = "Mahsulot narxini kiriting."
    await message.answer(text=text)
    await StickerState.price.set()


@dp.message_handler(state=StickerState.price, chat_id=ADMINS)
async def get_price_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "price": message.text
    })
    text = "Mahsulot haqida ma'lumot kiriting."
    await message.answer(text=text)
    await StickerState.description.set()


@dp.message_handler(state=StickerState.description, chat_id=ADMINS)
async def get_description_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "description": message.text
    })
    text = "Mahsulot sonini kiriting."
    await message.answer(text=text)
    await StickerState.quantity.set()


@dp.message_handler(state=StickerState.quantity, chat_id=ADMINS)
async def get_quantity_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "quantity": message.text
    })
    text = "Mahsulot rasmini kiriting."
    await message.answer(text=text)
    await StickerState.photo.set()


@dp.message_handler(state=StickerState.photo, chat_id=ADMINS, content_types=types.ContentType.PHOTO)
async def get_photo_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "photo": message.photo[-1].file_id
    })
    data = await state.get_data()
    if db_manager.append_product(data):
        text = "Mahsulot qo'shildi. ✅"
    else:
        text = "Mahsulot qo'shish jarayonida xatolik bor ❌"
    await message.answer(text=text, reply_markup=await admin_stickers_menu_def())
    await state.finish()


@dp.message_handler(chat_id=ADMINS, state="admin-stickers-state")
async def get_one_sticker_handler(message: types.Message):
    name = message.text
    sticker = db_manager.search_sticker_by_name(name)
    if sticker:
        sticker_id = sticker[0]
        name = sticker[1]
        price = sticker[2]
        description = sticker[3]
        photo = sticker[4]
        quantity = sticker[5]
        caption = f"{name} | {price} so'm | {quantity} ta bor\n\n{description}"
        await message.answer_photo(photo=photo, caption=caption,
                                   reply_markup=await admin_sticker_change_def(sticker_id))
