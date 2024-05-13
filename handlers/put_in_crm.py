from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.api import AmoCRM
from datetime import datetime
from keyboards.inline_keyboards import InlineMarkup


async def put_in_crm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await callback.message.edit_text(text="Отправляется...")
    w = data["master"]
    field_date = await AmoCRM.find_date(w.work)

    result = await AmoCRM.update_orders(work_id=w.work_id,
                                        enum_id=w.specialist_id,
                                        date_id=field_date['id'],
                                        data_value=datetime.now().timestamp(),
                                        orders=data['orders'])
    success = "<b>Успешно зачтены в смену:</b>\n\n"
    error = "<b>Ошибка при отправке:</b>\n\n"

    for res in result:
        if res[1]:
            success += res[0] + "\n"
        else:
            error += res[0] + '\n'

    if error != "<b>Ошибка при отправке:</b>\n\n":
        success += "\n" + error

    await callback.message.edit_text(text=success,
                                     reply_markup=await InlineMarkup.put_orders_again(),
                                     parse_mode=ParseMode.HTML)
