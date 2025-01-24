"""
router not included
"""


from aiogram import Router, types
from aiogram.filters import Command
from loader import db
from datetime import datetime, timedelta
from keyboards.inline import mandconfirm
from aiogram import types
from data import config
from ..scheduler import schedule_message

ts = Router()

@ts.message(Command("tetst"))
async def test(message: types.Message):
    channel = ("Life Logs", "https://t.me/notyuldshah")
    jid = schedule_message("there will be test\n\nhttps://t.me/notyuldshah", datetime.now() + timedelta(seconds=10), mandconfirm(channel))
    if jid != -1:
        await message.answer(f"Test scheduled (Job ID: {jid})")
    else:
        await message.answer("No posting channel found")

@ts.message(Command("test"))
async def test(message: types.Message):
    btns = [
        [
            types.InlineKeyboardButton(text="➖", callback_data="test:minus"),
            *[types.InlineKeyboardButton(text=f"{chr(65+i)}", callback_data=f"mcq_{i-65}") for i in range(config.MULTIPLE_CHOICE_DEF)],
            types.InlineKeyboardButton(text="➕", callback_data="test:plus")
        ],
        [
            types.InlineKeyboardButton(text="Switch to Open Ended", callback_data="switch_open"),
            types.InlineKeyboardButton(text="Allow multiple", callback_data="allow_multiple")
        ]
    ]
    for i in range(4):
        row = []
        for j in range(5):
            row.append(types.InlineKeyboardButton(text=f"{i*5+1+j}", callback_data=f"test_{i*5+1+j}"))
        btns.append(row)
    await message.answer("here should be a really long message because formatting may make it look like its stupid", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=btns))


@ts.message(Command("chs"))
async def chs(message: types.Message):
    chs = db.fetchall("SELECT * FROM channel")
    print(chs)