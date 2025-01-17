from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data import dict

btns1 = [
    [
        KeyboardButton(text=dict.exams)
    ],
    [
        KeyboardButton(text=dict.mands)
    ]
]

adm_default = ReplyKeyboardMarkup(keyboard=btns1, resize_keyboard=True)