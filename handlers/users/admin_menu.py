from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.admin_menu import admin_order_menu
from keyboards.inline.admin_keyboards import admin_order_decision_def, admin_order_accepted_def, \
    admin_order_canceled_def, admin_order_search_def
from loader import dp, db_manager


@dp.message_handler(text="Orders 🛍", chat_id=ADMINS)
async def admin_order_handler(message: types.Message):
    text = "Buyurtmalar menyusiga xush kelibsiz"
    await message.answer(text=text, reply_markup=admin_order_menu)


@dp.message_handler(text="WAITING ⏳", chat_id=ADMINS)
async def user_order_waiting_handler(message: types.Message):
    orders = db_manager.get_all_orders_by_status_admin("WAITING")

    if len(orders) == 0:
        text = "Hozirda buyurtmalar mavjud emas."
        await message.answer(text=text)
    else:
        for order in orders:
            order_items = db_manager.get_order_items_by_order_id(order[2])
            user = db_manager.get_user_by_id(order[1])
            products = ""
            counter = 1
            total_price = 0
            for item in order_items:
                total_price += float(item[4]) * float(item[3])
                products += f"{counter})\t {item[2]}\t| {item[4]} ta\t| {item[3]} so'm\n"
                counter += 1
            text = f"""

🆔 {order[2]}

☎️ {user[3]}
👤 {user[2]}
⏳ {order[3]}
⏰ {order[4]}

{products}
Jami: {total_price} so'm
    """
            await message.answer(text=text, reply_markup=await admin_order_decision_def(order[2], order[1]))


@dp.message_handler(text="ACCEPTED ✅", chat_id=ADMINS)
async def user_order_waiting_handler(message: types.Message):
    orders = db_manager.get_all_orders_by_status_admin("ACCEPTED")

    if len(orders) == 0:
        text = "Hozirda buyurtmalar mavjud emas."
        await message.answer(text=text)
    else:
        for order in orders:
            order_items = db_manager.get_order_items_by_order_id(order[2])
            user = db_manager.get_user_by_id(order[1])
            products = ""
            counter = 1
            total_price = 0
            for item in order_items:
                total_price += float(item[4]) * float(item[3])
                products += f"{counter})\t {item[2]}\t| {item[4]} ta\t| {item[3]} so'm\n"
                counter += 1
            text = f"""

🆔 {order[2]}

☎️ {user[3]}
👤 {user[2]}
⏳ {order[3]}
⏰ {order[4]}

{products}
Jami: {total_price} so'm
    """
            await message.answer(text=text, reply_markup=await admin_order_accepted_def(order[2], order[1]))


@dp.message_handler(text="CANCELED ❌", chat_id=ADMINS)
async def user_order_waiting_handler(message: types.Message):
    orders = db_manager.get_all_orders_by_status_admin("CANCELED")

    if len(orders) == 0:
        text = "Hozirda buyurtmalar mavjud emas."
        await message.answer(text=text)
    else:
        for order in orders:
            order_items = db_manager.get_order_items_by_order_id(order[2])
            user = db_manager.get_user_by_id(order[1])
            products = ""
            counter = 1
            total_price = 0
            for item in order_items:
                total_price += float(item[4]) * float(item[3])
                products += f"{counter})\t {item[2]}\t| {item[4]} ta\t| {item[3]} so'm\n"
                counter += 1
            text = f"""

🆔 {order[2]}

☎️ {user[3]}
👤 {user[2]}
⏳ {order[3]}
⏰ {order[4]}

{products}
Jami: {total_price} so'm
    """
            await message.answer(text=text, reply_markup=await admin_order_canceled_def(order[2], order[1]))


@dp.message_handler(text="Search 🔎", chat_id=ADMINS)
async def user_order_search_handler(message: types.Message, state: FSMContext):
    text = "Iltimos buyurtma ID raqamini kiriting."
    await message.answer(text=text)
    await state.set_state('admin-get-order-id')


@dp.message_handler(state="admin-get-order-id", chat_id=ADMINS)
async def user_order_get_id_handler(message: types.Message, state: FSMContext):
    order = db_manager.get_order_by_id(int(message.text))

    if order:
        text = ""
        order_items = db_manager.get_order_items_by_order_id(order[2])
        user = db_manager.get_user_by_id(order[1])
        products = ""
        counter = 1
        total_price = 0
        for item in order_items:
            total_price += float(item[4]) * float(item[3])
            products += f"{counter})\t {item[2]}\t| {item[4]} ta\t| {item[3]} so'm\n"
            counter += 1
        text += f"""
🆔 {order[2]}

☎️ {user[3]}
👤 {user[2]}
⏳ {order[3]}
⏰ {order[4]}

{products}
Jami: {total_price} so'm
"""
        await message.answer(text=text, reply_markup=await admin_order_search_def(order[2], order[1]))
    else:
        text = "Bu ID raqamli buyurtma mavjud emas. Iltimos ko'zinga qarab yozing."
        await message.answer(text=text)
    await state.finish()
