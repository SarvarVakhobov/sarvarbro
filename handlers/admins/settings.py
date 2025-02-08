import re
from aiogram import Router, types, F
from data import dict, config
from filters import IsAdmin, IsAdminCallback, CbData, CbDataStartsWith
from states import sets
from keyboards.inline import post_chan, set_menu, ping_set, mandconfirm, from_mans, back_inl_key
from keyboards.keyb import main_key, back_key
from aiogram.fsm.context import FSMContext
from loader import db, bot
from time import sleep
from aiogram import html
from states.admin_states import EditMessages
import json
from keyboards.inline.adminlines import ping_menu  # new import
from time import monotonic  # added import

set = Router()

set.message.filter(IsAdmin())
set.callback_query.filter(IsAdminCallback())
# bot.send_message(config.ADMINS[0], "Settings handler loaded", reply_parameters=)
@set.message(F.text == dict.settings)
async def sett(message: types.Message, state: FSMContext):
    await state.set_state(sets.smenu)
    await message.answer(f"Menu: <b>{dict.settings}</b>", reply_markup=main_key)
    # Removed posting channel text from the response
    response = "Here you can change some configuration settings"
    await message.answer(response, reply_markup=set_menu)

# --- Removed posting channel functionality ---
# Removed:
#   @set.callback_query(CbData("post"), sets.smenu)
#   @set.callback_query(CbData("set_new"), sets.post)
#   @set.message(F.text == dict.back, sets.link)
#   @set.message(sets.link)
#   @set.message(F.text == dict.back, sets.confirm)
#   @set.callback_query(CbData("reset"), sets.post)
#   @set.callback_query(CbData("sel_from"), sets.post)
#   @set.callback_query(CbDataStartsWith("select_"), sets.fmans)
#   @set.callback_query(CbData("back"), sets.fmans)
#   @set.callback_query(sets.confirm)
# --- End removed section ---

@set.callback_query(CbData("edit_start_msg"), sets.smenu)
async def edit_start_msg(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditMessages.waiting_for_start_msg)
    current = db.get_message_setting("start_msg")
    if current:
        msg_data = json.loads(current[0])
        if msg_data.get("type") == "text":
            current_msg = msg_data.get("content", "")
        else:
            current_msg = f"{msg_data.get('type')} message is set."
        instruction = f"Current Start Message:\n{current_msg}\n\nSend a new Start message to change it."
    else:
        instruction = "No Start message set. Send a new Start message to set it."
    await callback.message.delete()
    await callback.message.answer(instruction, reply_markup=back_key)
    # await state.update_data(msg_to_del=msg_to_del.message_id)
    await callback.answer("Editing Start message")

@set.callback_query(CbData("edit_success_msg"), sets.smenu)
async def edit_success_msg(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditMessages.waiting_for_success_msg)
    current = db.get_message_setting("success_msg")
    if current:
        msg_data = json.loads(current[0])
        if msg_data.get("type") == "text":
            current_msg = msg_data.get("content", "")
        else:
            current_msg = f"{msg_data.get('type')} message is set."
        instruction = f"Current Success Message:\n{current_msg}\n\nSend a new Success message to change it."
    else:
        instruction = "No Success message set. Send a new Success message to set it."
    await callback.message.delete()
    await callback.message.answer(instruction, reply_markup=back_key)
    # await state.update_data(msg_to_del=msg_to_del.message_id)
    await callback.answer("Editing Success message")

@set.message(F.text == dict.back, EditMessages.waiting_for_start_msg)
@set.message(F.text == dict.back, EditMessages.waiting_for_success_msg)
async def back_to_s(message: types.Message, state: FSMContext):
    # msg_to_del = (await state.get_data()).get("msg_to_del")
    # await message.bot.delete_message(message.chat.id, msg_to_del)
    await message.answer(f"Menu: <b>{dict.settings}</b>", reply_markup=main_key)
    await state.set_state(sets.smenu)
    await message.answer("Here you can change some configuration settings", reply_markup=set_menu)

@set.message(EditMessages.waiting_for_start_msg)
async def receive_start_message(message: types.Message, state: FSMContext):
    msg_data = {}
    if message.photo:
        msg_data["type"] = "photo"
        msg_data["file_id"] = message.photo[-1].file_id
        msg_data["caption"] = message.caption or ""
    elif message.video:
        msg_data["type"] = "video"
        msg_data["file_id"] = message.video.file_id
        msg_data["caption"] = message.caption or ""
    elif message.document:
        msg_data["type"] = "document"
        msg_data["file_id"] = message.document.file_id
        msg_data["caption"] = message.caption or ""
    elif message.animation:
        msg_data["type"] = "animation"
        msg_data["file_id"] = message.animation.file_id
        msg_data["caption"] = message.caption or ""
    elif message.text:
        msg_data["type"] = "text"
        msg_data["content"] = message.text
    else:
        await message.answer("Unsupported message type. Try sending text, photo, video, document or GIF.")
        return
    content_json = json.dumps(msg_data)
    db.update_message_setting("start_msg", content_json)
    await message.answer("Start message updated.")
    await state.set_state(sets.smenu)
    await message.answer("Here you can change some configuration settings", reply_markup=set_menu)
    # await state.clear()

@set.message(EditMessages.waiting_for_success_msg)
async def receive_success_message(message: types.Message, state: FSMContext):
    msg_data = {}
    if message.photo:
        msg_data["type"] = "photo"
        msg_data["file_id"] = message.photo[-1].file_id
        msg_data["caption"] = message.caption or ""
    elif message.video:
        msg_data["type"] = "video"
        msg_data["file_id"] = message.video.file_id
        msg_data["caption"] = message.caption or ""
    elif message.document:
        msg_data["type"] = "document"
        msg_data["file_id"] = message.document.file_id
        msg_data["caption"] = message.caption or ""
    elif message.animation:
        msg_data["type"] = "animation"
        msg_data["file_id"] = message.animation.file_id
        msg_data["caption"] = message.caption or ""
    elif message.text:
        msg_data["type"] = "text"
        msg_data["content"] = message.text
    else:
        await message.answer("Unsupported message type. Try sending text, photo, video, document or GIF.")
        return
    content_json = json.dumps(msg_data)
    db.update_message_setting("success_msg", content_json)
    await message.answer("Success message updated.")
    # await state.clear()
    await state.set_state(sets.smenu)
    await message.answer("Here you can change some configuration settings", reply_markup=set_menu)

@set.callback_query(CbData("ping"), sets.smenu)
async def ping(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(sets.ping)
    start_time = monotonic()
    sent_message = await callback.message.edit_text("Pinging... 🏓", reply_markup=back_inl_key)  # ensure back_inl_key is defined
    end_time = monotonic()
    ping_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    await sent_message.edit_text(f"Pong! 🏓\n\nPing: {html.code(f'{ping_ms:.2f} ms')}", reply_markup=ping_set)  # ensure ping_set is defined
    await callback.answer("Pinged!")

@set.callback_query(CbData("refresh_ping"), sets.ping)
async def refresh_ping(callback: types.CallbackQuery, state: FSMContext) -> None:
    start_time = monotonic()
    sent_message = await callback.message.edit_text("Pinging... 🏓", reply_markup=back_inl_key)
    end_time = monotonic()
    ping_ms = (end_time - start_time) * 1000
    await sent_message.edit_text(f"Pong! 🏓\n\nPing: {html.code(f'{ping_ms:.2f} ms')}", reply_markup=ping_set)
    await callback.answer("Pinged!")

@set.callback_query(CbData("back"), sets.ping)
async def back_to_s(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(sets.smenu)
    await callback.message.edit_text(
        "Here you can change some configuration settings, check the ping with the Telegram servers", 
        reply_markup=set_menu
    )
    await callback.answer("Back to settings menu")

