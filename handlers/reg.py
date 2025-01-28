from .admins import *
from .users import *
from .not_handled import remover

def register_handlers(dp):
    dp.include_routers(admin, ts, this_ro, mad, nosub, set, user, reger, remover)