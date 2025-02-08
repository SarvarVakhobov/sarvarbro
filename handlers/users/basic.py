import json
from aiogram import Router, types, F
from data import config, dict
from filters import IsUser, IsUserCallback, IsSubscriber, IsSubscriberCallback, CbData
from aiogram.filters import CommandStart, Command
from keyboards.keyb import user_markup
from aiogram.fsm.context import FSMContext
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

@user.callback_query(CbData("main_menu"))
async def main_menu(callback: types.CallbackQuery) -> None:
    await callback.message.answer("Main menu", reply_markup=user_markup)
    await callback.message.delete()

@user.message(Command("help"))
@user.message(F.text == dict.help_txt)
async def helpme(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    response = f"📚 Here is the help section."
    await message.answer(response)

@user.callback_query(CbData("check_subs"))
async def check_subs(callback: types.CallbackQuery) -> None:
    setting = db.get_message_setting("success_msg")
    if setting:
        msg_data = json.loads(setting[0])
        if msg_data["type"] == "text":
            await callback.message.answer(msg_data["content"], reply_markup=types.ReplyKeyboardRemove())
        elif msg_data["type"] == "photo":
            await callback.message.answer_photo(photo=msg_data["file_id"], caption=msg_data.get("caption", ""), reply_markup=types.ReplyKeyboardRemove())
        elif msg_data["type"] == "video":
            await callback.message.answer_video(video=msg_data["file_id"], caption=msg_data.get("caption", ""), reply_markup=types.ReplyKeyboardRemove())
        elif msg_data["type"] == "document":
            await callback.message.answer_document(document=msg_data["file_id"], caption=msg_data.get("caption", ""), reply_markup=types.ReplyKeyboardRemove())
        elif msg_data["type"] == "animation":
            await callback.message.answer_animation(animation=msg_data["file_id"], caption=msg_data.get("caption", ""), reply_markup=types.ReplyKeyboardRemove())
    else:
        await callback.message.answer("Thanks for joining the chats! You are now registered and can use all the functionalities of the bot!", reply_markup=types.ReplyKeyboardRemove())
    await callback.message.delete()