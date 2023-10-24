from aiogram import Dispatcher

from loader import dp
from .is_admin import AdminFilter
from .group_chat import IsGroup
from .private_chat import IsPrivate


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
