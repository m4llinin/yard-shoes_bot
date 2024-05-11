from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    ORDER_ID = State()
