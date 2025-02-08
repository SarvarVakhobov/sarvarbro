from .admins import *
from .admins.post import stater as post_router  # added registration for post router
from .users import *
from .users.notsub import nosub       # added import for unregistered handler
from .not_handled import remover

def register_handlers(dp):
    dp.include_routers(admin, mad, set, post_router, user, reger, nosub, remover)