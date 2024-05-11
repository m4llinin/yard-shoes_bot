from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from lexicon.lexicon_ru import lexicon
from keyboards.inline_keyboards import InlineMarkup


async def select_type(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=lexicon["specialist"], parse_mode=ParseMode.HTML,
                                     reply_markup=await InlineMarkup.select_type(state))


async def select_specialist(callback: CallbackQuery, state: FSMContext):
    data = callback.data.rsplit("-")
    await callback.message.edit_text(text=lexicon["schedule_specialist"].format(data[1]), parse_mode=ParseMode.HTML,
                                     reply_markup=await InlineMarkup.select_specialist(state, data[1]))
