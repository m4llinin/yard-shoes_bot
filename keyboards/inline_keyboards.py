from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.api import AmoCRM


class InlineMarkup:
    @classmethod
    async def start(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text="Занести работу", callback_data="put_orders")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def is_this_order(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text='Да', callback_data=f"yes"),
             InlineKeyboardButton(text='Нет', callback_data="find_again")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def find_again(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text="Добавить", callback_data="find_again")],
            [InlineKeyboardButton(text="Отправить", callback_data="put_in_crm")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def select_type(cls, state: FSMContext) -> InlineKeyboardMarkup:
        specialists = await AmoCRM.get_specialists()
        await state.update_data(specialists=specialists)
        keyboard = []
        for specialist in specialists:
            keyboard.append(
                [InlineKeyboardButton(text=specialist.title, callback_data=f"order-{specialist.title}")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def select_specialist(cls, state: FSMContext, stype: str) -> InlineKeyboardMarkup:
        data = await state.get_data()
        keyboard = []
        for work in data["specialists"]:
            if work.title == stype:
                for specialist in work.specialists:
                    keyboard.append([InlineKeyboardButton(text=specialist.name,
                                                          callback_data=f's-order-{work.title}-{work.id}-{specialist.name}')])
        keyboard.append([InlineKeyboardButton(text="Назад", callback_data="put_orders")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def put_orders_again(cls):
        keyboard = [
            [InlineKeyboardButton(text="Занести новую работу", callback_data="put_orders")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
