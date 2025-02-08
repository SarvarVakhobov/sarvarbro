import json
import asyncio
from aiogram.filters import Command
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import config, dict
from states.admin_states import BulkPost
from filters import IsAdmin, IsAdminCallback
from keyboards.keyb import back_key, main_key
from filters.customs import CbData
# from keyboards.inline import refresh
from loader import bot, db
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError

stater = Router()
stater.message.filter(IsAdmin())
stater.callback_query.filter(IsAdminCallback())

# Initiate bulk posting flow via /post command or when sending config.post
@stater.message(Command("post"))
@stater.message(F.text == dict.post)
async def initiate_bulk_post(message: types.Message, state: FSMContext):
    await state.set_state(BulkPost.waiting_for_message)
    await message.answer("Send the bulk message content (it may include photos, videos, documents or GIFs):", reply_markup=main_key)

# Capture bulk message content from admin
@stater.message(BulkPost.waiting_for_message)
async def capture_bulk_message(message: types.Message, state: FSMContext):
    bulk_data = {}
    # Check for media types and store only the file id plus caption if available.
    if message.photo:
        bulk_data["type"] = "photo"
        bulk_data["file_id"] = message.photo[-1].file_id
        bulk_data["caption"] = message.caption or ""
    elif message.video:
        bulk_data["type"] = "video"
        bulk_data["file_id"] = message.video.file_id
        bulk_data["caption"] = message.caption or ""
    elif message.document:
        bulk_data["type"] = "document"
        bulk_data["file_id"] = message.document.file_id
        bulk_data["caption"] = message.caption or ""
    elif message.animation:
        bulk_data["type"] = "animation"
        bulk_data["file_id"] = message.animation.file_id
        bulk_data["caption"] = message.caption or ""
    elif message.text:
        bulk_data["type"] = "text"
        bulk_data["content"] = message.text
    else:
        await message.answer("Unsupported message type. Try sending text, photo, video, document or GIF.")
        return

    # Store the minimal message info as JSON.
    content_json = json.dumps(bulk_data)
    await state.update_data(content=content_json)
    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Confirm", callback_data="bulk_confirm"),
         InlineKeyboardButton(text="Cancel", callback_data="bulk_cancel")]
    ])
    await message.answer("Do you confirm sending this bulk message?", reply_markup=confirm_kb)
    await state.set_state(BulkPost.waiting_for_confirmation)

# Confirm bulk post: store and start background processing
@stater.callback_query(CbData("bulk_confirm"))
async def confirm_bulk_post(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    content = data.get("content")
    bulk_id = db.add_bulk_message(content, "text")
    asyncio.create_task(start_bulk_posting(bulk_id, content))
    await callback.message.edit_text(f"Bulk message initiated with ID: {bulk_id}")
    await notify_admins(f"Bulk message with ID {bulk_id} has been initiated.")
    await state.clear()
    await callback.answer()

# Cancel bulk post
@stater.callback_query(CbData("bulk_cancel"))
async def cancel_bulk_post(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Bulk messaging cancelled.")
    await callback.answer()

# Background task: post to all users and notify admins after completion.
async def start_bulk_posting(bulk_id, content_json):
    content_data = json.loads(content_json)
    users = db.get_all_users()  # users as list of tuple with userid at index 0
    for user in users:
        uid = user[0]
        try:
            if content_data["type"] == "text":
                await bot.send_message(uid, content_data["content"])
            elif content_data["type"] == "photo":
                await bot.send_photo(uid, photo=content_data["file_id"], caption=content_data.get("caption", ""))
            elif content_data["type"] == "video":
                await bot.send_video(uid, video=content_data["file_id"], caption=content_data.get("caption", ""))
            elif content_data["type"] == "document":
                await bot.send_document(uid, document=content_data["file_id"], caption=content_data.get("caption", ""))
            elif content_data["type"] == "animation":
                await bot.send_animation(uid, animation=content_data["file_id"], caption=content_data.get("caption", ""))
            else:
                await bot.send_message(uid, "Unsupported message type.")
            await asyncio.sleep(0.5)  # avoid rate limits
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except TelegramForbiddenError:
            print(f"User {uid} blocked bot; skipping.")
    db.update_bulk_message_status(bulk_id, 1)
    await notify_admins(f"Bulk message with ID {bulk_id} has been completed.")

# Utility: Notify admins
async def notify_admins(msg):
    for admin in config.ADMINS:
        try:
            await bot.send_message(admin, msg)
        except Exception as e:
            print(f"Error notifying admin {admin}: {e}")

# Command to check bulk message status
@stater.message(Command("bulk_status"))
@stater.message(F.text == dict.bulk_status)
async def bulk_status(message: types.Message, state: FSMContext):
    # bulk_id = message.get_args()
    # if not bulk_id:
    await state.set_state(BulkPost.provide_id)
    await message.answer("Please provide the bulk message ID.", reply_markup=main_key)
        # return

    # # status = db.get_bulk_message_status(bulk_id)
    # if status:
    #     await message.answer(f"Bulk message status: {'Completed' if status[0] == 1 else 'In Progress'}")
    # else:
    #     await message.answer("Invalid bulk message ID.")

@stater.message(BulkPost.provide_id)
async def provide_bulk_id(message: types.Message, state: FSMContext):
    bulk_id = message.text
    status = None
    try:
        status = db.get_bulk_message_status(bulk_id)
    except Exception as e:
        print(f"Error getting bulk message status: {e}")
        await message.answer("Error getting bulk message status.\n\nPlease provide the bulk message ID.")
        # await state.clear()
        return
    if status:
        await message.answer(f"Bulk message status: {'Completed' if status[0] == 1 else 'In Progress'}")
    else:
        await message.answer("Invalid bulk message ID.")
    await state.clear()