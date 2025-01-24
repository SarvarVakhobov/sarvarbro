from aiogram import Router, types, html
from data import dict
from aiogram.filters import Command
from filters import IsSubscriber, IsSubscriberCallback, IsUser, IsUserCallback

this_ro = Router()

this_ro.message.filter(IsUser(), IsSubscriber())
this_ro.callback_query.filter(IsUserCallback(), IsSubscriberCallback())

@this_ro.message(Command("mag"))
async def mag(message: types.Message):
    response = f"{html.bold("№:")} 5\n{html.bold("Turi:")} Variantli\n\n{html.italic("Quyidagi tanlovlardan to'g'risini tanlang. Sahifalar orasida o'tish uchun tugmalar bilan foydalaning.")}"
    navigation_buttons = [
        types.InlineKeyboardButton(text="⏮️", callback_data="prev"),
        types.InlineKeyboardButton(text="⏪", callback_data="prev"),
        types.InlineKeyboardButton(text="1️⃣", callback_data="page_1"),
        types.InlineKeyboardButton(text="⏩", callback_data="next"),
        types.InlineKeyboardButton(text="⏭️", callback_data="next")
    ]

    btns = [
        [
            types.InlineKeyboardButton(text="Testga o'tish", url="https://t.me")
        ],
        [  # Row 1
            *[types.InlineKeyboardButton(text=f"{chr(65+i)}", callback_data=f"ans_{i}") for i in range(4)]
        ],
        [  # Row 2 (navigation buttons)
            *navigation_buttons
        ]
    ]
    for i in range(4):  # Loop through rows (excluding navigation row)
        row = []
        for j in range(5):
            if i * 5 + j + 1 == 20:
                row.append(types.InlineKeyboardButton(text="...", callback_data="next"))
                break  # Exit inner loop after adding "..." button
            emp = "✅ " if i * 5 + j + 1 < 10 else ""
            row.append(types.InlineKeyboardButton(text=f"{emp}{i * 5 + j + 1}", callback_data=f"ans_{i * 5 + j + 1}"))
        btns.append(row)

    await message.answer(response, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=btns))


@this_ro.message(Command("mag2"))
async def mag2(message: types.Message):
    btns = [
        [
            types.InlineKeyboardButton(text="👈 Orqaga", callback_data="adsf")
        ]
    ]

    await message.answer(f"Nom: {html.bold("SAT Math 1-test")}\nSavollar soni: {html.bold("22")}\n\nSiz ushbu testda quyidagi natijani ko'rsatdingiz:\n\t\tTo'g'ri javoblar soni: {html.italic('20')}\n\t\tSAT natija: {html.italic('780')}\n\t\tFoiz: {html.bold("91%")}\n\t\tTop: {html.italic("3% — 5 talik")}", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=btns))
    