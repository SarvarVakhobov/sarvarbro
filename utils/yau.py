from loader import db
from .chan_info import checksub

async def notsubbed(userid) -> list:
    channels = db.fetchall("SELECT title, chid, link FROM channel")
    new_chs = []
    for ch in channels:
        if not await checksub(userid, ch[1]):
            new_chs.append(ch)
    return new_chs