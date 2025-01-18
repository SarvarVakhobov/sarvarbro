from aiogram import Router, types
from aiogram.filters import Command
from filters import IsUser, IsUserCallback, IsNotSubscriber, IsNotSubscriberCallback
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
    response = "❕ You need to join the following chats to be able to use me."
    channels = await notsubbed(message.from_user.id)
    if channels:
        await message.answer(response, reply_markup=mand_chans(channels))
    else:
        await message.answer("Thanks for joinng the chats! You are now registered!")

@nosub.callback_query()
async def nuhuh_callback(callback: types.CallbackQuery) -> None:
    response = "❕ You need to join the following chats to be able to use me."
    channels = await notsubbed(callback.from_user.id)
    print(channels)
    if channels:
        if callback.data == "check_subs":
            response = "You didn't join all the following chats. Please join them to continue."
        try:
            await callback.message.edit_text(response, reply_markup=mand_chans(channels))
        except Exception as e:
            msg = await callback.message.answer("Please, don't spam the buttons.")
            sleep(2)
            await msg.delete()
        await callback.answer("Join the chats to proceed!")
    else:
        await callback.message.answer("Thanks for joinng the chats! You are now registered!")
        await callback.message.delete()
        await callback.answer("You are now registered!")
