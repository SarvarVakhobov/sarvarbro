from aiogram.types import ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner
from loader import bot

async def checksub(userid, chid):
    member = await bot.get_chat_member(chat_id=chid, user_id=userid)
    return member.status in [ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner]