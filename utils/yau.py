from loader import db
from .chan_info import checksub

def notsubbed(userid) -> list:
    channels = db.fetchall("SELECT title, link FROM channel")
    new_chs = []
    for ch in channels:
        if userid not in checksub(userid, ch[1]):
            new_chs.append(ch)
    return new_chs