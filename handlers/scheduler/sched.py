from datetime import datetime
from data import config
from aiogram import types
from loader import scheduler

async def send_scheduled_message(chat_id: int, text: str, markup: types.InlineKeyboardMarkup = None):
    msg = await bot.send_message(chat_id, text, reply_markup=markup)
    for idx in config.ADMINS:
        await bot.send_message(idx, "Scheduled message sent", reply_parameters=types.reply_parameters.ReplyParameters(chat_id=msg.chat_id, message_id=msg.message_id))
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: Sent scheduled message to {chat_id}: {text}")

def schedule(job, chat_id: int, text: str, schedule_time: datetime, markup: types.InlineKeyboardMarkup = None) -> int:
    j = scheduler.add_job(job, 'date', run_date=schedule_time, args=[chat_id, text])
    print(f"Scheduled message for chat_id {chat_id} at {schedule_time.strftime("%Y-%m-%d %H:%M:%S")}: {text}")
    return j.id