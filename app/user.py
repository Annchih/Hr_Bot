from aiogram import Router,F,Bot
import app.keyboards as kb
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from app.states import HrWait
from aiogram.fsm.context import FSMContext
from config import HR_ID
from app.db import db


user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    faqs = db.get_all_faqs()
    keyboard = kb.faq_keyboard(faqs)
    await message.answer(
        "Приветсвтую, я бот-помощник HR отдела компании ЦИТ-БАРС",
        reply_markup=keyboard
    )



@user.callback_query(F.data=='place')
async def place(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(
    "📍Наш офис находится по адресу:\n"
    "Пушкинская 268, домофон 52, 5 этаж")  
    await callback.message.answer_location(latitude=56.861316, longitude=53.209815)

@user.callback_query(F.data=='office')
async def place(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer( "<b>Видео-инструкция как найти вход:</b>\n"
    "<a href='https://vk.com/citbars?z=clip-152057105_456239094'>Смотреть видео</a>",
    parse_mode="HTML"
)

@user.callback_query(F.data=='ask_hr')
async def send_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напиши свой вопрос, я передам его нашему лучшему HR")
    await state.set_state(HrWait.InputState)
    await callback.answer('')

@user.message(HrWait.InputState)
async def forward_to_hr(message: Message, state: FSMContext):
    text = f"📩Новое сообщение от @{message.from_user.username or message.from_user.full_name}:\n\n{message.text}"
    await message.bot.send_message(HR_ID,text)
    await message.answer("Готово! HR скоро ответит😉")
    await state.clear()   


@user.callback_query(F.data.startswith("faq_"))
async def handle_faq_callback(callback: CallbackQuery):
    faq_id = int(callback.data.split("_")[1])
    question, answer = db.get_faq_by_id(faq_id)
    await callback.message.answer(f"<b>{question}</b> \n\n 💬{answer}", parse_mode="HTML")
    await callback.answer()