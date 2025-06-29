from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command
from aiogram.fsm.context import FSMContext
from config import ADMINS, HR_ID
from app.states import AddStates, EditStates, DeleteStates
from app.db import FAQManager



admin = Router()
db = FAQManager()

class Admin(Filter):
    async def __call__(self, message:Message):
        return message.from_user.id in ADMINS

class HR(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == HR_ID or message.from_user.id in ADMINS
    

@admin.message(Admin() or HR(), Command('add_question'))
async def add_question_start(message: Message, state: FSMContext):
    await message.answer("Введи текст нового вопроса:")
    await state.set_state(AddStates.add)

@admin.message(Admin(), AddStates.add)
async def add_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer("Теперь введи ответ на этот вопрос:")
    await state.set_state(AddStates.wait_answer)

@admin.message(Admin(), AddStates.wait_answer)
async def add_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    question = data.get("question")
    answer = message.text
    db.add_faq(question, answer)
    await message.answer("Вопрос с ответом успешно добавлены в FAQ!")
    await state.clear()

@admin.callback_query(Admin() or HR(), F.data.startswith("faq_"))
async def handle_faq(callback: CallbackQuery):
    faq_id = int(callback.data.split("_")[1])
    question, answer = db.get_faq_by_id(faq_id)
    await callback.message.answer(f"<b>{question}</b> \n\n 💬{answer}", parse_mode="HTML")
    await callback.answer()


@admin.message(Admin() or HR(),Command("edit_question"))
async def edit_question(message: Message, state: FSMContext):
    await message.answer("✏️ Введи текст вопроса, который хочешь изменить:")
    await state.set_state(EditStates.old_question)


@admin.message(Admin(),EditStates.old_question)
async def get_old_question(message: Message, state: FSMContext):
    await state.update_data(old_question=message.text)
    await message.answer("Введи новый текст вопроса:")
    await state.set_state(EditStates.new_question)

@admin.message(Admin(),EditStates.new_question)
async def get_new_question(message: Message, state: FSMContext):
    await state.update_data(new_question=message.text)
    await message.answer("Теперь введи новый ответ:")
    await state.set_state(EditStates.waiting_answer)

@admin.message(Admin(),EditStates.waiting_answer)
async def get_new_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    old_q = data["old_question"]
    new_q = data["new_question"]
    new_a = message.text

    faq_id = db.get_id_by_question(old_q)
    if faq_id is None:
        await message.answer("Не удалось найти такой вопрос.")
    else:
        db.update_faq(faq_id, question=new_q, answer=new_a)
        await message.answer("✅Вопрос успешно обновлён!")

    await state.clear()

@admin.message(Admin() or HR(),Command("delete_question"))
async def delete_question(message: Message, state: FSMContext):
    await message.answer("Введи текст вопроса, который хочешь удалить:")
    await state.set_state(DeleteStates.delete)


@admin.message(Admin(), DeleteStates.delete)
async def delete(message: Message, state: FSMContext):
    question = message.text
    faq_id = db.get_faq_by_question(question)

    if faq_id is None:
        await message.answer("Не удалось найти такой вопрос.")
    else:
        db.delete_faq(faq_id)
        await message.answer("Вопрос успешно удалён!")

    await state.clear()