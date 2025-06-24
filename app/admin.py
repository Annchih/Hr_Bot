from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command
from aiogram.fsm.context import FSMContext
from config import ADMINS
from app.states import AdminStates
from app.db import FAQManager

admin = Router()
db = FAQManager()

class Admin(Filter):
    async def __call__(self, message:Message):
        return message.from_user.id in ADMINS
    

@admin.message(Admin(), Command('add_question'))
async def add_question_start(message: Message, state: FSMContext):
    await message.answer("Введи текст нового вопроса:")
    await state.set_state(AdminStates.add)

@admin.message(Admin(), AdminStates.add)
async def add_question_receive(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer("Теперь введи ответ на этот вопрос:")
    await state.set_state(AdminStates.wait_answer)

@admin.message(Admin(), AdminStates.wait_answer)
async def add_answer_receive(message: Message, state: FSMContext):
    data = await state.get_data()
    question = data.get("question")
    answer = message.text
    db.add_faq(question, answer)
    await message.answer("Вопрос с ответом успешно добавлены в FAQ!")
    await state.clear()

@admin.callback_query(F.data.startswith("faq_"))
async def handle_faq_callback(callback: CallbackQuery):
    faq_id = int(callback.data.split("_")[1])
    question, answer = db.get_faq_by_id(faq_id)
    await callback.message.answer(f"<b>{question}</b> \n\n 💬{answer}", parse_mode="HTML")
    await callback.answer()