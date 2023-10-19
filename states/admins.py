from aiogram.dispatcher.filters.state import StatesGroup, State


class StickerState(StatesGroup):
    name = State()
    price = State()
    description = State()
    photo = State()
    quantity = State()


class StickerUpdateState(StatesGroup):
    name = State()
    price = State()
    description = State()
    photo = State()
    quantity = State()
    delete = State()
