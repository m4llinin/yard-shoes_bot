from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon_ru import lexicon
from keyboards.inline_keyboards import InlineMarkup
from utils.api import AmoCRM, Choice
from states.order import OrderStates
from datetime import datetime
from config import config


async def enter_name_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not ("master" in data):
        calldata = callback.data.rsplit("-")
        await state.update_data(master=Choice(work_id=int(calldata[3]),
                                              work=calldata[2],
                                              specialist_id=calldata[4]))
    await state.set_state(OrderStates.ORDER_ID)
    await callback.message.edit_text(text=lexicon['name_order'], parse_mode=ParseMode.HTML)


async def find_order(message: Message, state: FSMContext):
    await state.set_state(None)

    msg = await message.answer(text="Выполняется поиск...")
    order = await AmoCRM.find_order(message.text)
    await msg.delete()

    if order is None:
        await message.answer(text=lexicon['not_found'], parse_mode=ParseMode.HTML)
        return

    await message.answer(text=lexicon['schedule_order'].format(order['name'], order['price'],
                                                               datetime.fromtimestamp(order['created_at'],
                                                                                      tz=config.tz).strftime(
                                                                   '%H:%M %d.%m.%Y')),
                         parse_mode=ParseMode.HTML,
                         reply_markup=await InlineMarkup.is_this_order())
    await state.update_data(temp_order=order)


async def is_this_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if "orders" in data:
        data['orders'].append(data['temp_order'])
    else:
        data['orders'] = [data['temp_order']]
    await state.set_data(data)
    await callback.message.edit_text(text=lexicon["find_again"], reply_markup=await InlineMarkup.find_again())
