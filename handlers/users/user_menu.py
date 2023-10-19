from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.default.user_menu import user_stickers_menu_def
from keyboards.inline.admin_keyboards import admin_order_decision_def
from keyboards.inline.user_keyboards import user_product_buy_def, user_basket_menu
from loader import dp, db_manager
from utils.random_number import get_random_id


@dp.message_handler(text="💥 Stickers")
async def stickers_menu_handler(message: types.Message, state: FSMContext):
    await state.set_state('user-stickers-state')
    text = "Quyidagi stikerlardan birini tanlang."
    await message.answer(text=text, reply_markup=await user_stickers_menu_def())


@dp.message_handler(state="user-stickers-state")
async def get_one_sticker_handler(message: types.Message, state: FSMContext):
    name = message.text
    sticker = db_manager.search_sticker_by_name(name)
    if sticker:
        name = sticker[1]
        price = sticker[2]
        description = sticker[3]
        photo = sticker[4]
        quantity2 = sticker[5]

        data = await state.get_data()
        basket = data.get('basket') if data.get('basket') else dict()
        item = basket.get(name) if basket.get(name) else dict()
        quantity = item.get('quantity') if item.get('quantity') else 0
        total = item.get('total') if item.get('total') else 0
        await state.update_data({
            "product": name,
            "price": price
        })

        caption = f"{name} | {price} so'm | {quantity2} ta bor\n\n{description}"
        await message.answer_photo(photo=photo, caption=caption,
                                   reply_markup=await user_product_buy_def(quantity, total))


@dp.message_handler(text="🎥 Anime")
async def anime_sticker_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    basket = data.get('basket') if data.get('basket') else dict()
    item = basket.get("Anime") if basket.get("Anime") else dict()
    quantity = item.get('quantity') if item.get('quantity') else 0
    total = item.get('total') if item.get('total') else 0
    await state.update_data({
        "product": "Anime",
        "price": 40000
    })
    photo = "https://images.uzum.uz/chn1f256sfhndlbmra30/original.jpg"
    text = "😍 Anime\nStikerlar to'plami Naruto anime, 50 dona\nNarxi: 40000"
    await message.answer_photo(photo=photo, caption=text, reply_markup=await user_product_buy_def(quantity, total))


@dp.message_handler(text="😻 Cats")
async def cats_sticker_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    basket = data.get('basket') if data.get('basket') else dict()
    item = basket.get("Cats") if basket.get("Cats") else dict()
    quantity = item.get('quantity') if item.get('quantity') else 0
    total = item.get('total') if item.get('total') else 0
    await state.update_data({
        "product": "Cats",
        "price": 20000
    })
    photo = "https://images.uzum.uz/chp4ghlenntd8rfa8lrg/original.jpg"
    text = "😻 Cats\nStikerlar yoqimli mushuklar, mushuklar bilan nakleykalar, 6 dona\nNarxi: 20000"
    await message.answer_photo(photo=photo, caption=text, reply_markup=await user_product_buy_def(quantity, total))


@dp.callback_query_handler(text="plus_product", state="user-stickers-state")
async def plus_product_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = data.get('product')
    price = data.get('price')
    basket = data.get('basket') if data.get('basket') else dict()
    item = basket.get(product) if basket.get(product) else dict()
    quantity = item.get('quantity') if item.get('quantity') else 0
    if quantity == 10:
        text = "Bitta zakazda bitta mahsulotdan 10 tadan ko'p olish" \
               " qatiyan man etiladi. Hurmat bilan BACK-425 guruhi"
        await call.answer(text=text, show_alert=True)
    else:
        quantity += 1
        basket[product] = {
            "quantity": quantity,
            "price": price,
            "total": price * quantity,
            "name": product
        }
        await state.update_data({
            "basket": basket
        })
        text = "Mahsulot bittaga ko'paydi xo'jayin"
        await call.answer(text=text)
        await call.message.edit_reply_markup(reply_markup=await user_product_buy_def(quantity, quantity * price))


@dp.callback_query_handler(text="minus_product", state="user-stickers-state")
async def minus_product_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = data.get('product')
    price = data.get('price')
    basket = data.get('basket') if data.get('basket') else dict()
    item = basket.get(product) if basket.get(product) else dict()
    quantity = item.get('quantity') if item.get('quantity') else 0
    if quantity == 0:
        text = "0 dan kam bo'lishi mumkin emas"
        await call.answer(text=text, show_alert=True)
    else:
        quantity -= 1
        basket[product] = {
            "quantity": quantity,
            "price": price,
            "total": price * quantity,
            "name": product
        }
        await state.update_data({
            "basket": basket
        })
        text = "Mahsulot bittaga kamaydi xo'jayin"
        await call.answer(text=text)
        await call.message.edit_reply_markup(reply_markup=await user_product_buy_def(quantity, quantity * price))


@dp.callback_query_handler(text="show_basket", state="user-stickers-state")
async def show_product_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    basket = data.get('basket')
    if basket:
        text = "Sizning savatingizda quyidagi mahsulotlar bor: \n\n"
        counter = 1
        total = 0
        for product in basket.values():
            text += f"<i><b>{counter}) {product['name']}\t| {product['quantity']} ta " \
                    f"\t| {product['price']} so'm\t| {product['total']} so'm\n</b></i>"
            counter += 1
            total += product['total']
        text += f"\nJami: {total} so'm"

        await call.message.answer(text=text, reply_markup=user_basket_menu)
    else:
        text = "Sizning savatingizda hech narsa mavjud emas. ❗️"
        await call.answer(text=text, show_alert=True)


@dp.callback_query_handler(text="clear_basket", state="user-stickers-state")
async def clear_basket_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "basket": dict()
    })
    popup = "Savat tozalandi ❗️"
    await call.answer(text=popup, show_alert=True)
    text = "Sizning savatingizda quyidagi mahsulotlar bor: "
    await call.message.edit_text(text=text)


@dp.callback_query_handler(text="order_basket", state="user-stickers-state")
async def order_basket_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    basket = data.get('basket')
    user = db_manager.get_user(call.message)
    order_id = get_random_id()
    if basket and user:
        text = "Sizning zakazingiz quyidagi ko'rinishda: \n"
        text += f"""
ID: {order_id}
FI: {user[2]}
TEL: {user[3]}
SANA: {call.message.date}
STATUS: WAITING

"""
        counter = 1
        total = 0
        for product in basket.values():
            text += f"<i><b>{counter}) {product['name']}\t| {product['quantity']} ta " \
                    f"\t| {product['price']} so'm\t| {product['total']} so'm\n</b></i>"
            counter += 1
            total += product['total']
        text += f"\nJami: {total} so'm"

        await state.update_data({
            "basket": dict()
        })
        new_order = db_manager.append_order(call.message, basket, order_id)
        if not new_order:
            admin_text = "Zakazlarni bazaga qo'shish joyida xatolik chiqdi"
            await dp.bot.send_message(text=admin_text, chat_id=ADMINS[0])

        await dp.bot.send_message(chat_id=ADMINS[0], text=text,
                                  reply_markup=await admin_order_decision_def(order_id, call.message.chat.id))
        await call.message.answer(text=text)
    else:
        text = "Sizning savatingizda hech narsa mavjud emas. ❗️"
        await call.answer(text=text, show_alert=True)
