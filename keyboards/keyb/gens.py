from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data import dict

btns1 = [
    [
        KeyboardButton(text=dict.back)
    ]
]

back_keys = ReplyKeyboardMarkup(keyboard=btns1, resize_keyboard=True)

