from aiogram import F, Router
from aiogram.filters import CommandStart

from .start import start
from .find_order import enter_name_order, find_order, is_this_order
from .get_specialist import select_type, select_specialist
from .put_in_crm import put_in_crm

from states.order import OrderStates


def register_handlers(router: Router) -> None:
    router.message.register(start, CommandStart())

    router.callback_query.register(select_type, F.data == "put_orders")
    router.callback_query.register(select_specialist, lambda query: query.data.startswith("order-"))

    router.callback_query.register(enter_name_order, lambda query: query.data.startswith("s-order-"))
    router.message.register(find_order, F.text, OrderStates.ORDER_ID)

    router.callback_query.register(enter_name_order, F.data == "find_again")
    router.callback_query.register(is_this_order, F.data == "yes")
    router.callback_query.register(put_in_crm, F.data == "put_in_crm")
