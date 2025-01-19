import re
from aiogram import Router, types, F
from data import dict, config
from filters import IsAdmin, IsAdminCallback, CbData, CbDataStartsWith
from states import sets
from keyboards.inline import post_chan, set_menu, mandconfirm, from_mans
from keyboards.keyb import main_key, back_key
from aiogram.fsm.context import FSMContext
from loader import db, bot
from time import sleep

set = Router()

set.message.filter(IsAdmin())
set.callback_query.filter(IsAdminCallback())

@set.message(F.text == dict.settings)
async def sett(message: types.Message, state: FSMContext):
    await state.set_state(sets.smenu)
    await message.answer(f"Menu: <b>{dict.settings}</b>", reply_markup=main_key)
    response = "Here you can change some configuration settings and manage posting channel"
    await message.answer(response, reply_markup=set_menu)

@set.callback_query(CbData("post"), sets.smenu)
async def post_c(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(sets.post)
    response = "Here you can change or reset the posting channel"
    channel = db.fetchone("SELECT title, link FROM channel WHERE post > 0")
    print(channel)
    if not channel:
        response = "Posting channel was not set, you can set it in two ways"
    await callback.message.edit_text(response, reply_markup=post_chan(channel))

@set.callback_query(CbData("back"), sets.post)
async def back_to_s(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(sets.smenu)
    # await callback.message.answer(f"Menu: <b>{dict.settings}</b>", reply_markup=main_key)
    response = "Here you can change some configuration settings and manage posting channel"
    await callback.message.edit_text(response, reply_markup=set_menu)
    await callback.answer("Back to settings menu")

@set.callback_query(CbData("set_new"), sets.post)
async def setnew(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(sets.link)
    await callback.message.answer("Send the link to the channel you want to set as posting channel in following formats:\n\t\tUsername: <code>username</code>\n\t\tUsername with @: <code>@username</code>\n\t\tPublic link: <code>https://t.me/username</code>\n\nOr forward a message from the chat to here (Better for private chats)", reply_markup=back_key)
    await callback.message.delete()

@set.message(F.text == dict.back, sets.link)
async def back_to_c(message: types.Message, state: FSMContext):
    await state.set_state(sets.post)
    await message.answer("Back to posting channel menu", reply_markup=main_key)
    response = "Here you can change or reset the posting channel"
    channel = db.fetchone("SELECT title, link FROM channel WHERE post > 0")
    if not channel:
        response = "Posting channel was not set, you can set it in two ways"
    await message.answer(response, reply_markup=post_chan(channel))

@set.message(sets.link)
async def get_link(message: types.Message, state: FSMContext):
    USERNAME_PATTERN = r"^[a-zA-Z][\w\d_]{4,31}$"  # Username (e.g., channelname)
    AT_USERNAME_PATTERN = r"^@[a-zA-Z][\w\d_]{4,31}$"  # Username starting with @
    # PRIVATE_LINK_PATTERN = r"^https://t\.me/\+\w+$"  # Private links (e.g., https://t.me/+W3UbzATqipEzYTVi)
    PUBLIC_LINK_PATTERN = r"^https://t\.me/[a-zA-Z][\w\d_]{4,31}$"  # Public links (e.g., https://t.me/channelname)
    text = None
    lk = None
    chanid = None
    # print(message.forward_from_chat)
    if message.forward_from_chat:
        chanid = message.forward_from_chat.id
        if message.forward_from_chat.username == None:
            try:
                lk = (await bot.create_chat_invite_link(chat_id=chanid, name=f"Join link by {config.bot_info.username}")).invite_link
            except Exception as e:
                print(e)
                await message.answer("Please, make sure to add the bot to the chat as an admin and try again")
                return
        else:
            lk = f"https://t.me/{message.forward_from_chat.username}"
    else:
        text = message.text 
        if re.match(USERNAME_PATTERN, text):
            # chanid = (await bot.get_chat("@"+text)).id
            uname = "@"+text
            lk = f"https://t.me/{text}"
        elif re.match(AT_USERNAME_PATTERN, text):
            uname = text
            # chanid = (await bot.get_chat(text)).id
            lk = f"https://t.me/{text[1:]}"
        elif re.match(PUBLIC_LINK_PATTERN, text):
            # chanid = (await bot.get_chat("@"+text[13])).id
            uname = "@"+text[13:]
            lk = text
        else:
            await message.answer("Invalid link format. Please, send the link of the chat to add in one of the following formats:\n\t\tUsername: <code>username</code>\n\t\tUsername with @: <code>@username</code>\n\t\tPublic link: <code>https://t.me/username</code>\n\nOr forward a message from the chat to here (Better for private chats)")
            return
        try:
            chanid = (await bot.get_chat(uname)).id
        except:
            await message.answer("Chat not found, make sure chat exists and bot is an admin in the chat")
            return
    data = await state.get_data()
    try:
        channel_info = await bot.get_chat(chanid)
        mb_cnt = await bot.get_chat_member_count(chanid)
        mebot = await bot.get_chat_member(chat_id=chanid, user_id=config.bot_info.id)
    except Exception as e:
        print(e)
        print(lk)
        await message.answer("Please, make sure to add the bot to the chat as an admin, chat exists and try again")
        return
    # print(title, lk)
    title = channel_info.title
    
    await state.set_state(sets.confirm)
    await state.update_data(title=title)
    await state.update_data(link=lk)
    await state.update_data(chid=chanid)
    # print(title, lk)
    await message.answer(f"Check and confirm everything is correct\n\nChat Information:"
            f"\n\t\tTitle: {channel_info.title}"
            f"\n\t\tMembers count: {mb_cnt}"
            f"\n\t\tDescription: <code>{channel_info.description or 'No description'}</code>", reply_markup=mandconfirm((title, lk)), disable_web_page_preview=True)

@set.message(F.text == dict.back, sets.confirm)
async def back_to_link(message: types.Message, state: FSMContext) -> None:
    await state.set_state(sets.link)
    await message.answer("Now send the right link", reply_markup=back_key)

@set.callback_query(CbData("reset"), sets.post)
async def reset(callback: types.CallbackQuery, state: FSMContext) -> None:
    old = db.fetchone("SELECT title, link, chid, post FROM channel WHERE post > 0")
    if old and old[3]==1:
        db.query("DELETE FROM channel WHERE chid = ?", (old[2],))
    else:
        db.query("UPDATE channel SET post = 0 WHERE chid = ?", (old[2],))
    await callback.answer("Reset successfull")
    await post_c(callback, state)

@set.callback_query(CbData("sel_from"), sets.post)
async def selfro(callback: types.CallbackQuery, state: FSMContext) -> None:
    channels = db.fetchall("SELECT title, link, idx, post FROM channel WHERE NOT post = 1")
    if channels:
        await state.set_state(sets.fmans)
        await callback.message.edit_text("Select a channel from the list to set as posting channel", reply_markup=from_mans(channels))
    else:
        await callback.answer("❌ No mandatory channels to select from")
    # old = db.fetchone("SELECT title, link, chid FROM channel WHERE post > 0")
    
@set.callback_query(CbDataStartsWith("select_"), sets.fmans)
async def setfro(callback: types.CallbackQuery, state: FSMContext) -> None:
    idx = int(callback.data.split("_")[1])
    channel = db.fetchone("SELECT title, post FROM channel WHERE idx = ?", (idx,))
    if channel:
        if channel[1]!=0:
            msg = await callback.message.answer(f"This channel already has been set as the posting channel")
            await callback.answer("Back to posting channel menu")
            await post_c(callback, state)
            sleep(2)
            await msg.delete()
            return
        db.query("UPDATE channel SET post = 2 WHERE idx = ?", (idx,))
        await callback.answer(f"Successfully set {channel[0]} as posting channel")
        # await callback.message.edit_text("Back to posting channel menu", reply_markup=main_key)
        await post_c(callback, state)
    else:
        await callback.answer("❌ Channel not found")

@set.callback_query(CbData("back"), sets.fmans)
async def back_to_post(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer("Back to posting channel menu")
    await post_c(callback, state)

@set.callback_query(sets.confirm)
async def confirm(callback: types.CallbackQuery, state: FSMContext) -> None:
    if callback.data == "cancel":
        await callback.answer("Cancelled")
        await callback.message.answer("Back to posting channel menu", reply_markup=main_key)
        await post_c(callback, state)
        # await callback.message.delete()
        return
    data = await state.get_data()
    chid = data.get("chid")
    title = data.get("title")
    link = data.get("link")
    chck = db.fetchone("SELECT title FROM channel WHERE chid = ? AND post > 0", (chid,))
    if chck:
        msg = await callback.message.answer(f"This channel already has been set as the posting channel")
        await callback.answer("Already posting channel")
        await callback.message.answer("Back to posting channel menu", reply_markup=main_key)
        await post_c(callback, state)
        sleep(2)
        await msg.delete()
        # await callback.message.delete()
        return
    # channel_info = await bot.get_chat(link)
    old = db.fetchone("SELECT title, link, chid, post FROM channel WHERE post > 0")
    print(old)
    if old:
        if old[3]==1:
            db.query("DELETE FROM channel WHERE chid = ?", (old[2],))
        else:
            db.query("UPDATE channel SET post = 0 WHERE chid = ?", (old[2],))
    sme = db.fetchone("SELECT post FROM channel WHERE chid = ?", (chid,))
    print(sme)
    if sme:
        print("Updating")
        db.query("UPDATE channel SET post = 2 WHERE chid = ?", (chid,))
    else:
        db.query("INSERT INTO channel (chid, title, link, post) VALUES (?, ?, ?, 1)", (chid, title, link))
    await callback.answer(f"Successfully set")
    await callback.message.answer("Back to posting channel menu", reply_markup=main_key)
    await post_c(callback, state)
    # await callback.message.delete()

