from aiogram import Router
from aiogram.types import Message, CallbackQuery
remover = Router()

@remover.message()
async def remove(message: Message) -> None:
    msg = await message.reply("Not recognized")
    from time import sleep
    sleep(2)
    try:
        await msg.delete()
        await message.delete()
    except Exception as e:
        print(f"Couldnt be deleted\n\nHere is the message:\n\n{message}\n\nHere is the error:\n\n{e}")
@remover.callback_query()
async def remove_callback(callback: CallbackQuery) -> None:
    await callback.answer("Not recognized")
    await callback.message.delete()