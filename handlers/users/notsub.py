from aiogram import Router, types
from aiogram.filters import Command
from filters import IsUser, IsUserCallback, IsNotSubscriber, IsNotSubscriberCallback, CbData
from keyboards.inline import mand_chans
from loader import db
from utils.yau import notsubbed
from time import sleep

nosub = Router()

nosub.message.filter(IsUser(), IsNotSubscriber())
nosub.callback_query.filter(IsUserCallback(), IsNotSubscriberCallback())

@nosub.message(Command("help"))
async def helpme(message: types.Message) -> None:
    response = f"📚 Here is the help section. You can send a message only once!"
    await message.answer(response)

@nosub.message()
async def nuhuh(message: types.Message) -> None:
    await message.answer("❗️ You need to join the following chats to be able to use me.", reply_markup=types.ReplyKeyboardRemove())
    response = "After joining all the chats provided, press the \"✓ Check\" button below."
    channels = await notsubbed(message.from_user.id)
    if channels:
        await message.answer(response, reply_markup=mand_chans(channels))
    else:
        await message.answer("Thanks for joinng the chats! You are now registered!")

@nosub.callback_query(CbData("check_subs"))
async def nuhuh_callback(callback: types.CallbackQuery) -> None:
    # response = "❗️ You need to join the following chats to be able to use me."
    response = "🚫 You didn't join all the following chats. Please join them to continue."
    channels = await notsubbed(callback.from_user.id)
    await callback.answer("🚫 Join the chats to proceed!")
    try:
        await callback.message.edit_text(response, reply_markup=mand_chans(channels))
    except Exception as e:
        msg = await callback.message.answer("❗️ Please, don't spam the buttons.")
        sleep(2)
        await msg.delete()