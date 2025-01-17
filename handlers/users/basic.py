from aiogram import Router, types, F
from data import config, dict
from filters import IsUser, IsUserCallback, IsRegistered
from aiogram.filters import CommandStart, Command
# from keyboards.keyboard import user_markup, end_markup
# from keyboards.inline import create_url_button, open_ban
from aiogram.fsm.context import FSMContext
# from states import conv_states
from loader import db


user = Router()


user.message.filter(IsUser(), IsRegistered())
user.callback_query.filter(IsUserCallback())

@user.message(CommandStart())
@user.message(F.text == dict.main_menu)
async def welcome(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    # alr = db.fetchone("SELECT * FROM users WHERE userid=?", (message.from_user.id,))
    # conv = db.fetchone("SELECT COUNT(idx) FROM chats WHERE userid=?", (message.from_user.id,))[0]
    response = f"👋 Heyy, <b>{message.from_user.first_name}</b>. Welcome back to the bot!"
    await message.answer(response)

@user.message(Command("help"))
@user.message(F.text == dict.help_txt)
async def helpme(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    response = f"📚 Here is the help section."
    await message.answer(response)