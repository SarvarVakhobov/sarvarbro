# can be used later to add phone numbers of the users later

from aiogram import types, Router
from filters import IsNotRegistered, IsUser
from loader import db
from keyboards.inline import mand_chans
from utils.yau import notsubbed
# from keyboards.keyboard import user_markup

reger = Router()

reger.message.filter(IsNotRegistered(), IsUser())

@reger.message()
async def process_command(message: types.Message) -> None:
    db.query("INSERT INTO users (userid, fullname, username) VALUES (?, ?, ?)", (message.from_user.id, message.from_user.full_name, message.from_user.username))
    response = f"👋 Heyy, <b>{message.from_user.first_name}</b>."
    channels = notsubbed(message.from_user.id)
    if channels:
        response += "\n\n❕ You need to join the following chats to be able to use me."
        await message.answer(response, reply_markup=mand_chans(channels))
    else:
        response += "\n\n🎉 You are now registered!"
        await message.answer(response)