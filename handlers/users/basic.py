from aiogram import Router, types, F
from data import config, dict
from filters import IsUser, IsUserCallback, IsSubscriber, IsSubscriberCallback, CbData
from aiogram.filters import CommandStart, Command
from keyboards.keyb import user_markup
# from keyboards.inline import create_url_button, open_ban
from aiogram.fsm.context import FSMContext
# from states import conv_states
from loader import db


user = Router()


user.message.filter(IsUser(), IsSubscriber())
user.callback_query.filter(IsUserCallback(), IsSubscriberCallback())

@user.message(CommandStart())
@user.message(F.text == dict.main_menu)
async def welcome(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    print(message.from_user.mention_html)
    # alr = db.fetchone("SELECT * FROM users WHERE userid=?", (message.from_user.id,))
    # conv = db.fetchone("SELECT COUNT(idx) FROM chats WHERE userid=?", (message.from_user.id,))[0]
    response = f"👋 Salom, <b>{message.from_user.mention_html()}</b>. Botga xush kelibsiz!"
    await message.answer(response, reply_markup=user_markup)

@user.message(Command("help"))
@user.message(F.text == dict.help_txt)
async def helpme(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    response = f"📚 Here is the help section."
    await message.answer(response)

@user.callback_query(CbData("check_subs"))
async def check_subs(callback: types.CallbackQuery) -> None:
    await callback.message.answer("Thanks for joining the chats! You are now registered and can use all the functionalities of the bot!", reply_markup=user_markup)
    await callback.message.delete()