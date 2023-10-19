from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    full_name = State()
    phone_number = State()
    modme_id = State()
    parol = State()
    group_number = State()
    group_type = State()


class ProfileUpdate(StatesGroup):
    full_name = State()
    phone_number = State()
    group_number = State()
    group_type = State()