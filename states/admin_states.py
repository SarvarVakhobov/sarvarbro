from aiogram.fsm.state import State, StatesGroup

class mands(StatesGroup):
    title = State()
    link = State()
    confirm = State()