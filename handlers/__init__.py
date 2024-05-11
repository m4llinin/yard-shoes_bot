from aiogram import F, Router
from aiogram.filters import CommandStart

from .start import start
from .find_order import enter_name_order, find_order
from .get_specialist import select_type, select_specialist

from states.order import OrderStates


def register_handlers(router: Router) -> None:
    router.message.register(start, CommandStart())

    router.callback_query.register(enter_name_order, F.data == "find_order")
    router.message.register(find_order, F.text, OrderStates.ORDER_ID)

    router.callback_query.register(select_type, F.data == "yes")
    router.callback_query.register(select_specialist, lambda query: query.data.startswith("order-"))
