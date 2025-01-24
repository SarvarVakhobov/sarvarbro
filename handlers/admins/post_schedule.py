from aiogram import types, Router, F
from data import dict
from filters import IsAdmin, IsAdminCallback
from states import edits

psch = Router()

psch.message.filter(IsAdmin())
psch.callback_query.filter(IsAdminCallback())

