from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data import dict


def mandchans(channels = []):
    # channels = db.fetchall("SELECT title, link FROM channels")
    btns = []
    cnt = 1
    for channel in channels:
        btns.append([
                InlineKeyboardButton(text=channel[0], url=channel[1]),
                InlineKeyboardButton(text=dict.edit, callback_data=f"edit_{cnt}"),
                InlineKeyboardButton(text=dict.delete, callback_data=f"delete_{cnt}")
            ])
    btns.append([InlineKeyboardButton(text=dict.add_chat, callback_data="add_chat")])
    return InlineKeyboardMarkup(inline_keyboard=btns)