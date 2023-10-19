from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token="6020804140:AAHfrwN_soXYLwpQjy5nYd-v3Z9AeU3MMRM")
dp = Dispatcher(bot)

location_keyboard = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Lokatsiya jo'natish", request_location=True)
    ]], resize_keyboard=True
)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Lokatsiya kiriting.", reply_markup=location_keyboard)


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def echo_message(message: types.Message):
    longitude = message.location.longitude
    latitude = message.location.latitude

    await message.answer_location(longitude=longitude, latitude=latitude)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
