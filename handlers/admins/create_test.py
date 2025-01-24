from pyexpat.errors import messages

from data import config
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data.config import MAX_EXAMS_AT_A_TIME
from utils.yau import g_code
from keyboards.inline import confirm_admin, all_checked, one_checked
from keyboards.keyb import main_key, back_key, skip_desc
from states import creates
from loader import db
from filters import IsAdmin, IsAdminCallback

crt = Router()
crt.message.filter(IsAdmin())
crt.callback_query.filter(IsAdminCallback())

@crt.message(F.text == dict.cr_test)
async def create_test(message: types.Message, state: FSMContext):
    response = "Please, send the title of the test:"
    await state.set_state(creates.title)
    await message.answer(response, reply_markup=main_key)

@crt.message(creates.title)
async def take_title(message: types.Message, state: FSMContext):
    t = message.text
    await state.update_data(title=t)
    await state.set_state(creates.about)
    await message.answer(f"<b>Title:</b> {t}\n\nPlease, send the description", reply_markup=skip_desc)

@crt.message(creates.about, F.text == dict.back)
async def back_to_title(message: types.Message, state: FSMContext):
    await state.set_state(creates.title)
    await create_test(message, state)

@crt.message(creates.about, F.text == config.skip)
async def skip_to_questnum(message: types.Message, state: FSMContext):
    title = await state.get_data("title")
    await state.update_data(about_skip=1)
    await state.set_state(creates.number)
    await message.answer(f"<b>Title:</b> {title}\n<s>Description skipped</s>\n\nPlease, send the number of questions:", reply_markup=back_key)

@crt.message(creates.about)
async def about(message: types.Message, state: FSMContext):
    title = await state.get_data("title")
    a = message.text
    await state.update_data(about=a)
    await state.update_data(about_skip=0)
    await state.set_state(creates.number)
    await message.answer(f"<b>Title:</b> {title}\n<b>Description:</b> {a}\n\nPlease, send the number of questions:", reply_markup=back_key)

@crt.message(creates.number, F.text == config.back)
async def back_to_about(message: types.Message, state: FSMContext):
    response = f"<b>Title:</b> {await state.get_data('title')}"
    response += "\n\nPlease, send the description:"
    await state.set_state(creates.about)
    await message.answer(response, reply_markup=skip_desc)

@crt.message(creates.number)
async def process_num(message: types.Message, state: FSMContext):
    try:
        num = int(message.text)
    except Exception:
        await message.answer("Please, enter a valid number")
        return
    if 0 < num <= 50:
        # data = await state.get_data()
        response = f"<b>Title:</b> {await state.get_data('title')}"
        response += "" if int(await state.get_data("about_skip")) else f"\n<b>Description:</b> {await state.get_data("about")}"
        response += f"\n<b>Number of questions:</b> {num}\n\n"
        await state.update_data(num_quest=num)
        await state.set_state(creates.ans)
        await state.update_data(mode=1)
        await state.update_data(current=1)
        await state.update_data(correct="")
        response += "You can send the correct answers in either of this way. Change as you please and send them:"
        await message.answer(response, reply_markup=all_checked)
    else:
        await message.answer("Please, enter a number in range of 1 to 50 to provide good user experience")

@crt.message(creates.correct_answer, F.text == config.back)
async def back_to_num(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data["current"] > 1:
        cnt = data["current"]
        await state.update_data(current=cnt-1)
        correct = data["correct"]
        if cnt == 2:
            await state.update_data(correct="")
        else:
            correct = correct[:-2-correct[::-1].find("__")]
            await state.update_data(correct=correct)
        await message.answer(f"Send the answer for question number <b>{cnt-1}</b>")
    else:
        response = f"<b>Title:</b> {data['title']}"
        response += f"\n<b>Description:</b> {data['about']}" if data['about'] != "__skip" else ""
        response += "\n\nPlease, enter the number of questions:"
        await state.set_state(creates.number)
        await message.answer(response, reply_markup=back_key)

@crt.callback_query(creates.correct_answer)
async def process_checking(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    n = data["current"]
    if callback.data == "all_at_one_checked":
        await callback.answer("Already chosen")
    elif callback.data == "one_by_one":
        await callback.answer("One by one")
        await state.update_data(mode=2)
        await callback.message.answer(f"Send the answer for question number <b>{n}</b>")
        await callback.message.edit_reply_markup(reply_markup=one_checked)
    elif callback.data == "one_by_one_checked":
        await callback.answer("Already chosen")
    elif callback.data == "all_at_one":
        await callback.answer("All at one")
        await state.update_data(mode=1)
        await callback.message.answer(f"<b>{n-1}</b> answers were given with one-by-one method. Please, send the others, starting with the answer for question number {n}, at once.")
        await callback.message.edit_reply_markup(reply_markup=all_checked)

@crt.message(creates.correct_answer)
async def taking_answers(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cnt = data["current"]
    n_questions = int(data["num_quest"])
    if data["mode"] == 1:
        raw = message.text.split("\n")
        correct = data["correct"]
        for line in range(len(raw)):
            if raw[line] != "":
                correct += ("__" if cnt > 1 else "") + raw[line]
                cnt += 1
        if cnt == n_questions + 1:
            await state.update_data(correct=correct)
            await state.set_state(creates.confirm)
            await message.answer(f"Can you confirm your actions?", reply_markup=confirm_admin)
        else:
            await message.answer("The number of questions doesn't match the entered value. Please, enter correct number of answers or change the number of questions.", reply_markup=back_key)
    else:
        correct = data["correct"]
        correct += ("__" if cnt > 1 else "") + message.text
        await state.update_data(correct=correct)
        if cnt == n_questions:
            await state.set_state(creates.confirm)
            await message.answer("You have done entering all the answers. Can you confirm your actions?", reply_markup=confirm_admin)
        else:
            cnt += 1
            await state.update_data(current=cnt)
            await message.answer(f"Send the answer for question number <b>{cnt}</b>")

@crt.callback_query(creates.confirm)
async def create_confirm(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if callback.data == "admin_confirm":
        corr = data["correct"]
        n_questions = int(data["num_quest"])
        title = data["title"]
        ab = data["about"]
        code = g_code()
        from_db = db.fetchone("SELECT * FROM exams WHERE code = ?", (code,))
        while from_db is not None:
            code = g_code()
            from_db = db.fetchone("SELECT * FROM exams WHERE code = ?", (code,))
        db.query("INSERT INTO exams(code, title, about, num_questions, correct, running) VALUES (?,?,?,?,?,?)", (code, title, ab, n_questions, corr, 1))
        await callback.message.answer("Test created. Check the test in the ⚡️ Running tests menu")
        await callback.answer("Confirmed")
    elif callback.data == "admin_cancel":
        await callback.message.answer("Test creation cancelled")
        await callback.answer("Cancelled")
    await callback.bot.send_message(callback.message.chat.id, "You've been brought to 🏠 Main menu.", reply_markup=main_key)
    await callback.message.delete()
    await state.clear()

@crt.message(creates.confirm, F.text == config.back)
async def back_to_receiving(message: types.Message, state: FSMContext):
    data = await state.get_data()
    response = f"<b>Title:</b> {data['title']}"
    response += f"\n<b>Description:</b> {data['about']}" if data['about'] != "__skip" else ""
    response += f"\n<b>Number of questions:</b> {data['num_quest']}\n\n"
    await state.set_state(creates.correct_answer)
    await state.update_data(mode=1)
    await state.update_data(current=1)
    await state.update_data(correct="")
    response += "You can send the correct answers in either of this way. Change as you please and send them:"
    await message.answer(response, reply_markup=all_checked)