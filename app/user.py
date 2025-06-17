from aiogram import Router,F
from app.keyboards import faq
from aiogram.types import Message
from aiogram.filters import CommandStart
user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Приветсвтую, я бот-помщник HR отдела, компании ЦИТ-БАРС")





