from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from lexicon.lexicon_ru import lexicon
from keyboards.inline_keyboards import InlineMarkup


async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=lexicon['start'].format(message.from_user.first_name),
                         reply_markup=await InlineMarkup.start(), parse_mode=ParseMode.HTML)
