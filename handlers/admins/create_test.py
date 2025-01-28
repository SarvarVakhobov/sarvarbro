from aiogram import Router, types, F, html
from data import dict, config
from filters import IsAdmin, IsAdminCallback, CbData, CbDataStartsWith
from aiogram.fsm.context import FSMContext
from loader import db
from states import creates
from utils.yau import ber
from keyboards.keyb import back_key, main_key, skip_desc
from keyboards.inline import ans_enter_meth, obom

crtest = Router()

crtest.message.filter(IsAdmin())
crtest.callback_query.filter(IsAdminCallback())

@crtest.message(F.text == dict.cr_test)
async def create_test(message: types.Message, state: FSMContext) -> None:
    response = "Please, send the title of the test:"
    await state.set_state(creates.title)
    await message.answer(response, reply_markup=main_key)

@crtest.message(creates.title)
async def take_title(message: types.Message, state: FSMContext) -> None:
    t = message.text
    response = f"Title: {html.bold(f"{t}")}\n\nPlease, send the description"
    await state.update_data(title=t)
    await state.set_state(creates.about)
    await message.answer(response, reply_markup=skip_desc)

@crtest.message(creates.about, F.text == dict.back)
async def back_to_title(message: types.Message, state: FSMContext) -> None:
    response = "Please, send the right title of the test:"
    await state.set_state(creates.title)
    await message.answer(response, reply_markup=main_key)

@crtest.message(creates.about, F.text == dict.skip)
async def skip_to_instructions(message: types.Message, state: FSMContext) -> None:
    await state.update_data(about_skip=1)
    await state.set_state(creates.instructions)
    response = f"Title: {html.bold(f'{await ber(state, "title")}')}\n\nPlease, send the instructions for users:"
    await message.answer(response, reply_markup=skip_desc)

@crtest.message(creates.about)
async def about(message: types.Message, state: FSMContext) -> None:
    title = await ber(state, "title")
    a = message.text
    await state.update_data(about=a)
    await state.update_data(about_skip=0)
    await state.set_state(creates.instructions)
    response = f"Title: {html.bold(f'{title}')}\nDescription: {html.bold(f'{a}')}\n\nPlease, send the instructions for users:"
    await message.answer(response, reply_markup=skip_desc)

@crtest.message(creates.instructions, F.text == dict.back)
async def back_to_about(message: types.Message, state: FSMContext) -> None:
    response = f"Title: {html.bold(f'{await ber(state, 'title')}')}\n\nPlease, send the description:"
    await state.set_state(creates.about)
    await message.answer(response, reply_markup=skip_desc)

@crtest.message(creates.instructions, F.text == dict.skip)
async def skip_to_questnum(message: types.Message, state: FSMContext) -> None:
    await state.update_data(instructions_skip=1)
    await state.set_state(creates.number)
    response = f"Title: {html.bold(f'{await ber(state, "title")}')}{f"\nDescription: {html.bold(f'{await ber(state, 'about')}')}" if await ber(state, "about_skip") == 0 else ""}\n\nPlease, send the number of questions:"
    await message.answer(response, reply_markup=back_key)

@crtest.message(creates.instructions)
async def instructions(message: types.Message, state: FSMContext) -> None:
    title = await ber(state, "title")
    instructions = message.text
    await state.update_data(instructions=instructions)
    await state.update_data(instructions_skip=0)
    await state.set_state(creates.number)
    response = f"Title: {html.bold(f'{title}')}{f"\nDescription: {html.bold(f'{await ber(state, 'about')}')}" if await ber(state, "about_skip") == 0 else ""}\nInstructions: {html.bold(f'{instructions}')}\n\nPlease, send the number of questions:"
    await message.answer(response, reply_markup=back_key)

@crtest.message(creates.number, F.text == dict.back)
async def back_to_instructions(message: types.Message, state: FSMContext) -> None:
    response = f"Title: {html.bold(f'{await ber(state, 'title')}')}{f"\nDescription: {html.bold(f'{await ber(state, 'about')}')}" if await ber(state, "about_skip") == 0 else ""}\n\nPlease, send the instructions for users:"
    await state.set_state(creates.instructions)
    await message.answer(response, reply_markup=skip_desc)

@crtest.message(creates.number)
async def process_num(message: types.Message, state: FSMContext) -> None:
    try:
        num = int(message.text)
    except Exception:
        await message.answer("Please, enter a valid number")
        return
    if 0 < num <= 100:
        response = f"Title: {html.bold(f'{await ber(state, 'title')}')}{f"\nDescription: {html.bold(f'{await ber(state, 'about')}')}" if await ber(state, "about_skip") == 0 else ""}{f"\nInstructions: {html.bold(f'{await ber(state, 'instructions')}')}" if await ber(state, "instructions_skip") == 0 else ""}\nNumber of questions: {html.bold(f'{num}')}\n\n"
        await state.update_data(num_quest=num)
        await state.set_state(creates.way)
        response += "You can send the correct answers in either of this way. Please choose which way you want to send the answers:"
        await message.answer(response, reply_markup=ans_enter_meth)
    else:
        await message.answer("Please, enter a number in range of 1 to 100 to provide good user experience. Contact the developer if you need to create a test with more questions.")


@crtest.message(creates.way, F.text == dict.back)
async def back_to_number(message: types.Message, state: FSMContext) -> None:
    response = f"Title: {html.bold(f'{await ber(state, 'title')}')}{f"\nDescription: {html.bold(f'{await ber(state, 'about')}')}" if await ber(state, "about_skip") == 0 else ""}{f"\nInstructions: {html.bold(f'{await ber(state, 'instructions')}')}" if await ber(state, "instructions_skip") == 0 else ""}\n\nPlease, send the number of questions:"
    await state.set_state(creates.number)
    await message.answer(response, reply_markup=back_key)

@crtest.callback_query(CbData("all"))
async def all_at_once(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(f"Please, send the answers in the following format:\n\n{html.code("Answer1\nAnswer2\nAnswer3,Answer3Alternative\nAnswer4")}")
    await state.update_data(mode=1)

@crtest.callback_query(CbData("one"))
async def one_by_one(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Please, send the first answer:", reply_markup=obom(4, 23, [1, 2, 3]))
    await state.update_data(mode=2)