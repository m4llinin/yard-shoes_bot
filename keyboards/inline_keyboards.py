from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.api import AmoCRM


class InlineMarkup:
    @classmethod
    async def start(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text="Найти сделку", callback_data="find_order")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def is_this_order(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text='Да', callback_data=f"yes"),
             InlineKeyboardButton(text='Нет', callback_data="find_order")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def find_again(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text="Найти еще раз", callback_data="find_again")]
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
        keyboard.append([InlineKeyboardButton(text="Новый поиск", callback_data="find_order")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    async def select_specialist(cls, state: FSMContext, stype: str) -> InlineKeyboardMarkup:
        data = await state.get_data()
        keyboard = []
        for Type in data["specialists"]:
            if Type.title == stype:
                for specialist in Type.specialists:
                    keyboard.append([InlineKeyboardButton(text=specialist.name,
                                                          callback_data=f's-order-{Type.title}-{Type.id}-{specialist.id}')])
        keyboard.append([InlineKeyboardButton(text="Назад", callback_data="yes")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
