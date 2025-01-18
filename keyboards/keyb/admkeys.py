from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data import dict

btns1 = [
    [
        KeyboardButton(text=dict.cr_test)
    ],
    [
        KeyboardButton(text=dict.running_exams),
        KeyboardButton(text=dict.archive)
    ],
    [
        KeyboardButton(text=dict.exams),
        KeyboardButton(text=dict.mands)
    ],
    [
        KeyboardButton(text=dict.settings),
        KeyboardButton(text=dict.help_txt),
        KeyboardButton(text=dict.stats)
    ]
]

adm_default = ReplyKeyboardMarkup(keyboard=btns1, resize_keyboard=True)