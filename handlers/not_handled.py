from aiogram import Router
from aiogram.types import Message, CallbackQuery
from keyboards.keyb import main_key

remover = Router()

@remover.message()
async def remove(message: Message) -> None:
    await message.reply("Not recognized", reply_markup=main_key)
    print(f"Not handled message: {message}")
@remover.callback_query()
async def remove_callback(callback: CallbackQuery) -> None:
    await callback.message.answer("Not recognized", reply_markup=main_key)
    await callback.answer("Not recognized")