from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

faq = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Где мы находимся?', callback_data='place')],
    [InlineKeyboardButton(text='Не смогли найти вход? Как нас найти?', callback_data='office')],
    [InlineKeyboardButton(text='Другой вопрос? Задать вопрос HR', callback_data='ask_hr')],
])


welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписаться')]
])
