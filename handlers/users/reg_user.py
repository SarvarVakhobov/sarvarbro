# can be used later to add phone numbers of the users later

from aiogram import types, Router
from filters import IsNotRegistered, IsUser
from loader import db
# from keyboards.keyboard import user_markup

reger = Router()

reger.message.filter(IsNotRegistered(), IsUser())

@reger.message()
async def process_command(message: types.Message) -> None:
    db.query("INSERT INTO users (userid, fullname, username) VALUES (?, ?, ?)", (message.from_user.id, message.from_user.full_name, message.from_user.username))
    response = f"👋 Heyy, <b>{message.from_user.first_name}</b>."
    await message.answer(response)