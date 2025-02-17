from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from data import config
from loader import db, bot
from utils.chan_info import checksub

class IsRegistered(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return db.fetchone("SELECT idx FROM users WHERE userid=?", (message.from_user.id,)) != None

class IsNotRegistered(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # print(db.fetchone("SELECT idx FROM users WHERE userid=?", (message.from_user.id,)))
        return db.fetchone("SELECT idx FROM users WHERE userid=?", (message.from_user.id,)) == None

class IsSubscriber(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_row = db.fetchone("SELECT subscribed FROM users WHERE userid=?", (message.from_user.id,))
        if user_row and user_row[0] == 1:
            return True
        channels = db.fetchall("SELECT chid FROM channel")
        for ch in channels:
            if not await checksub(message.from_user.id, ch[0]):
                return False
        return True

class IsNotSubscriber(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        channels = db.fetchall("SELECT chid FROM channel")
        for ch in channels:
            if not await checksub(message.from_user.id, ch[0]):
                return True
        return False

class IsSubscriberCallback(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        user_row = db.fetchone("SELECT subscribed FROM users WHERE userid=?", (callback.from_user.id,))
        if user_row and user_row[0] == 1:
            return True
        channels = db.fetchall("SELECT chid FROM channel")
        for ch in channels:
            if not await checksub(callback.from_user.id, ch[0]):
                return False
        return True

class IsNotSubscriberCallback(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        channels = db.fetchall("SELECT chid FROM channel")
        for ch in channels:
            if not await checksub(callback.from_user.id, ch[0]):
                return True
        return False

class IsAdmin(BaseFilter):
    # def __init__(self, args):
    #     print(args)
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in config.ADMINS and message.chat.type == "private"
    
class IsAdminCallback(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.from_user.id in config.ADMINS and callback.message.chat.type == "private"

class IsUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        res = message.from_user.id not in config.ADMINS
        return res and message.chat.type == "private"

class IsUserCallback(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        res = callback.from_user.id not in config.ADMINS
        return res and callback.message.chat.type == "private"