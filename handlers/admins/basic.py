from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from filters import IsAdmin, IsAdminCallback
from aiogram.fsm.context import FSMContext
from data import dict
from loader import db

admin = Router()

admin.message.filter(IsAdmin())
admin.callback_query.filter(IsAdminCallback())

@admin.message(CommandStart())
async def adminstart(message: types.Message) -> None:
    await message.answer("Hello, admin")

@admin.message(F.text == dict.mands)
async def pmands(message: types.Message) -> None:
    response = "There are no mandatory chats to join right now. You can add from here"
    channels = db.fetchall("SELECT title, link FROM channels")
    if channels:
        