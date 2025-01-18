from aiogram import Router, types, F
from filters import IsAdmin, IsAdminCallback, CbData, CbDataStartsWith
from data import dict
from aiogram.fsm.context import FSMContext
from states import mands

mad = Router()

mad.message.filter(IsAdmin)
# mad.callback_query.filter(IsAdminCallback)

@mad.callback_query(CbData("add_chat"))
async def add_chat(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(mands.title)
    await callback.message.answer("Send the title of the chat to add")

@mad.message(mands.title)
async def add_chat_title(message: types.Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(mands.link)
    await message.answer("Send the link of the chat to add in one of the following formats:\n\tUsername: <code>username</code>\n\tUsername with @: <code>@username</code>\n\tPrivate link: <code>https://t.me/+AbCdEfGhIj</code>\n\tPublic link: <code>https://t.me/username</code>")

@mad.message(mands.link)
async def confirm(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    title = data.get("title")
    link = message.text
    await state.finish()
    await message.answer(f"Added the chat with title: {title} and link: {link}")