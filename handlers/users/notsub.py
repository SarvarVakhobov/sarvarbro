from aiogram import Router, types
from aiogram.filters import Command
from filters import IsUser, IsNotSubscriber, IsNotSubscriberCallback
from keyboards.inline import mand_chans
from loader import db
from utils.yau import notsubbed

nosub = Router()

nosub.message.filter(IsUser(), IsNotSubscriber())
nosub.callback_query.filter(IsUser(), IsNotSubscriberCallback())

@nosub.message(Command("help"))
async def helpme(message: types.Message) -> None:
    response = f"📚 Here is the help section. You can send a message only once!"
    await message.answer(response)

@nosub.message()
async def nuhuh(message: types.Message) -> None:
    response = "❕ You need to join the following chats to be able to use me."
    channels = notsubbed(message.from_user.id)
    if channels:
        await message.answer(response, reply_markup=mand_chans(channels))
    else:
        await message

@nosub.callback_query()
async def nuhuh_callback(callback: types.CallbackQuery) -> None:
    response = "❕ You need to join the following chats to be able to use me."
    channels = notsubbed(callback.from_user.id)
    if channels:
        if callback.data == "check_subs":
            response = "You didn't join all the following chats. Please join them to continue."
        await callback.message.edit_text(response, reply_markup=mand_chans(channels))
        await callback.answer()
    else:
        await callback.message.answer("Thanks for joinng the chats! You are now registered!")
        await callback.message.delete()
        await callback.answer("You are now registered!")