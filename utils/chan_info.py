from aiogram.types import ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner
from loader import bot

async def checksub(userid, chid):
    # print(chid, userid)
    member = await bot.get_chat_member(chat_id=chid, user_id=userid)
    # print(type(member.status), member.status in [ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner])
    return member.status in ["member", "creator", "owner", "administrator"]