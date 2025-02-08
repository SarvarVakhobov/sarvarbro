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
    ping = State()
    fmans = State()
    del_con = State()

class creates(StatesGroup):
    title = State()
    about = State()
    instructions = State()  # New state added
    number = State()
    way = State()
    ans = State()

class edits(StatesGroup):
    emenu = State()
    edit = State()
    title = State()
    about = State()
    edans = State()
    share = State()
    post = State()

class BulkPost(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirmation = State()

    #check status

    provide_id = State()
    

class EditMessages(StatesGroup):
    waiting_for_start_msg = State()
    waiting_for_success_msg = State()