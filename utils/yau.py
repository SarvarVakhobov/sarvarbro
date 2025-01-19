from loader import db
from .chan_info import checksub
import random
import string

async def notsubbed(userid) -> list:
    channels = db.fetchall("SELECT title, chid, link FROM channel WHERE NOT post = 1")
    new_chs = []
    for ch in channels:
        if not await checksub(userid, ch[1]):
            new_chs.append(ch)
    return new_chs

def g_code():
    characters = string.ascii_letters + string.digits  # Letters and digits
    return ''.join(random.sample(characters, 6))