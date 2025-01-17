from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from filters import IsAdmin, IsAdminCallback
from aiogram.fsm.context import FSMContext
from data import dict
from loader import db
from keyboards.inline import mandchans
from keyboards.keyb import adm_default

admin = Router()

admin.message.filter(IsAdmin())
admin.callback_query.filter(IsAdminCallback())

@admin.message(CommandStart())
async def adminstart(message: types.Message) -> None:
    await message.answer("Hello, admin", reply_markup=adm_default)

@admin.message(F.text == dict.mands)
async def pmands(message: types.Message) -> None:
    response = "There are no mandatory chats to join right now. You can add from here"
    channels = db.fetchall("SELECT title, link FROM channels")
    if channels:
        response = "Following are the mandatory chats to join. You can add new, edit or delete existing ones."
    await message.answer(response, reply_markup=mandchans(channels))