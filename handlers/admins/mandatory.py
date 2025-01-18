import re
from aiogram import Router, types, F
from filters import IsAdmin, IsAdminCallback, CbData, CbDataStartsWith
from data import dict
from aiogram.fsm.context import FSMContext
from states import mands, dels
from keyboards.inline import mandconfirm
from loader import bot, db

mad = Router()

mad.message.filter(IsAdmin())
# mad.callback_query.filter(IsAdminCallback)

@mad.callback_query(CbData("add_chat"))
async def add_chat(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(mands.title)
    await callback.message.answer("Send the title of the chat to add")

@mad.message(mands.title)
async def add_chat_title(message: types.Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(mands.link)
    await message.answer("Send the link of the chat to add in one of the following formats:\n\t\tUsername: <code>username</code>\n\t\tUsername with @: <code>@username</code>\n\t\tPrivate link: <code>https://t.me/+AbCdEfGhIj</code>\n\t\tPublic link: <code>https://t.me/username</code>")

@mad.message(mands.link)
async def getlink(message: types.Message, state: FSMContext) -> None:
    USERNAME_PATTERN = r"^[a-zA-Z][\w\d_]{4,31}$"  # Username (e.g., channelname)
    AT_USERNAME_PATTERN = r"^@[a-zA-Z][\w\d_]{4,31}$"  # Username starting with @
    PRIVATE_LINK_PATTERN = r"^https://t\.me/\+\w+$"  # Private links (e.g., https://t.me/+W3UbzATqipEzYTVi)
    PUBLIC_LINK_PATTERN = r"^https://t\.me/[a-zA-Z][\w\d_]{4,31}$"  # Public links (e.g., https://t.me/channelname)
    text = message.text.strip()
    lk = None
    if re.match(USERNAME_PATTERN, text):
        lk = f"https://t.me/{text}"
    elif re.match(AT_USERNAME_PATTERN, text):
        lk = f"https://t.me/{text[1:]}"
    elif re.match(PRIVATE_LINK_PATTERN, text):
        lk = text
    elif re.match(PUBLIC_LINK_PATTERN, text):
        lk = text
    else:
        await message.answer("Invalid link format. Please, send the link of the chat to add in one of the following formats:\n\t\tUsername: <code>username</code>\n\t\tUsername with @: <code>@username</code>\n\t\tPrivate link: <code>https://t.me/+AbCdEfGhIj</code>\n\t\tPublic link: <code>https://t.me/username</code>")
        return
    data = await state.get_data()
    title = data.get("title")
    
    try:
        channel_info = await bot.get_chat("@"+lk[13:])
        mb_cnt = await bot.get_chat_member_count(channel_info.id)
    except Exception as e:
        await message.answer("Please, make sure to add the bot to the chat as an admin and try again")
        print(e)
        print(lk)
        return
    await state.set_state(mands.confirm)
    await state.update_data(link=lk)
    await state.update_data(chid=channel_info.id)
    await message.answer(f"Check and confirm everything is correct\n\nChat Information:"
            f"\n\t\tTitle: {channel_info.title}"
            f"\n\t\tMembers count: {mb_cnt}"
            f"\n\t\tDescription: <code>{channel_info.description or 'No description'}</code>", reply_markup=mandconfirm((title, lk)), disable_web_page_preview=True)

@mad.callback_query(mands.confirm)
async def confirm(callback: types.CallbackQuery, state: FSMContext) -> None:
    if callback.data == "cancel":
        await state.clear()
        await callback.answer("Cancelled")
        await callback.message.delete()
        return
    data = await state.get_data()
    chid = data.get("chid")
    title = data.get("title")
    link = data.get("link")
    # channel_info = await bot.get_chat(link)
    db.query("INSERT INTO channel (chid, title, link) VALUES (?, ?, ?)", (chid, title, link))
    await callback.message.answer(f"Successfully added")
    await callback.message.delete()
    await state.clear()


@mad.callback_query(CbDataStartsWith("delete_"))
async def delete_chat(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(dels.confirm)
    cnt = int(callback.data.split("_")[1])
    channel = db.fetchone("SELECT * FROM channel WHERE idx=?", (cnt,))
    if not channel:
        await callback.answer("Channel not found")
        return
    # await state.set_state(mands.delete)
    await state.update_data(idx=channel[0])
    await callback.message.answer(f"Are you sure you want to delete the chat?", reply_markup=mandconfirm((channel[2], channel[3])), disable_web_page_preview=True)

@mad.callback_query(dels.confirm)
async def confirm_delete(callback: types.CallbackQuery, state: FSMContext) -> None:
    if callback.data == "cancel":
        await state.clear()
        await callback.answer("Cancelled")
        await callback.message.delete()
        return
    data = await state.get_data()
    idx = data.get("idx")
    db.query("DELETE FROM channel WHERE idx=?", (idx,))
    await callback.message.answer(f"Successfully deleted")
    await callback.message.delete()
    await state.clear()