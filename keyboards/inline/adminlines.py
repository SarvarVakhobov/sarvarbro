from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data import dict, config


def mandchans(channels = []):
    # channels = db.fetchall("SELECT title, link FROM channels")
    btns = []
    for channel in channels:
        btns.append([
                InlineKeyboardButton(text=channel[0], url=channel[1]),
                InlineKeyboardButton(text=dict.delete, callback_data=f"delete_{channel[2]}")
            ])
    btns.append([InlineKeyboardButton(text=dict.add_chat, callback_data="add_chat")])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def mandconfirm(channel):
    btns = [
        [
            InlineKeyboardButton(text=channel[0], url=channel[1])
        ],
        [
            InlineKeyboardButton(text=dict.cancel, callback_data="cancel"),
            InlineKeyboardButton(text=dict.confirm, callback_data="confirm")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=btns)

btns1 = [
    [
        InlineKeyboardButton(text="🆕 Not sub", callback_data="edit_start_msg"),
        InlineKeyboardButton(text="🎉 Success", callback_data="edit_success_msg")
    ],
    [
        InlineKeyboardButton(text="🏓 Ping", callback_data="ping")
    ]
]
# Added inline buttons to initiate editing the start and success messages
# btns1.append([
    
# ])
# # Add a row with Ping button
# btns1.append()
set_menu = InlineKeyboardMarkup(inline_keyboard=btns1)

def post_chan(channel):
    btns = []
    if channel:
        btns.append([InlineKeyboardButton(text=channel[0], url=channel[1])])
        btns.append([InlineKeyboardButton(text=dict.reset, callback_data="reset")])
    btns.append([InlineKeyboardButton(text=dict.sel_from_man, callback_data="sel_from"), InlineKeyboardButton(text=dict.set_new, callback_data="set_new")])
    btns.append([InlineKeyboardButton(text=dict.back, callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=btns)

def from_mans(channels):
    btns = []
    for channel in channels:
        btns.append([InlineKeyboardButton(text=channel[0], url=channel[1]), InlineKeyboardButton(text=dict.select, callback_data=f"select_{channel[2]}")])
    btns.append([InlineKeyboardButton(text=dict.back, callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=btns)

btns2 = [
    [
        InlineKeyboardButton(text=dict.all_at_one, callback_data="all"),
        InlineKeyboardButton(text=dict.one_by_one, callback_data="one")
    ]
]
ans_enter_meth = InlineKeyboardMarkup(inline_keyboard=btns2)

# def obom(cur, numq, type, multen, mcqnum, mcqans, page=1):
#     btns = []
#     arow = [InlineKeyboardButton(text="-", callback_data="test:minus")]
#     if type == 1:
#         for i in range(mcqnum):
#             arow.append(InlineKeyboardButton(text=f"{chr(65+i)}{}", callback_data=f"mcq_{i-65}"))
#         arow.append(*[InlineKeyboardButton(text=f"{chr(65+i)}", callback_data=f"mcq_{i-65}") for i in range(config.MULTIPLE_CHOICE_DEF)])
#     arow.append(InlineKeyboardButton(text="+", callback_data="test:plus"))
#     btns.append(arow)
#     btns.append(
#         # [
#         #     ,
#         #     ,
#         #     InlineKeyboardButton(text="+", callback_data="test:plus")
#         # ],
#         [
#             InlineKeyboardButton(text="Switch to Open Ended", callback_data="switch_open") if type == 1 else InlineKeyboardButton(text="Switch to Multiple Choice", callback_data="switch_mcq"),
#             InlineKeyboardButton(text="Allow multiple", callback_data="allow_multiple") if not multen else InlineKeyboardButton(text="Disallow multiple", callback_data="disallow_multiple") 
#         ]
#     )
#     for i in range((numq+19)//20):
#             row.append(InlineKeyboardButton(text=f"{i*5+1+j}", callback_data=f"test_{i*5+1+j}"))
#         btns.append(row)

# New function: returns inline keyboard with Refresh and Back buttons for ping
def ping_menu():
    btns = [
        [
            InlineKeyboardButton(text="Refresh", callback_data="refresh_ping"),
            InlineKeyboardButton(text="Back", callback_data="back_from_settings")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=btns)

btns3 = [
    [
        InlineKeyboardButton(text=dict.back, callback_data="back"),
        InlineKeyboardButton(text=dict.refresh_txt, callback_data="refresh_ping")
    ]
]
ping_set = InlineKeyboardMarkup(inline_keyboard=btns3)