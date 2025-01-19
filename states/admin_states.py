from aiogram.fsm.state import State, StatesGroup

class mands(StatesGroup):
    mmenu = State()
    title = State()
    link = State()
    confirm = State()

class dels(StatesGroup):
    confirm = State()

class sets(StatesGroup):
    smenu = State()
    post = State()
    link = State()
    confirm = State()
    fmans = State()
    del_con = State()