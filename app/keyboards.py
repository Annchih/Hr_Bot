from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

faq = InlineKeyboardMarkup[
    [InlineKeyboardButton(text='Где мы находимся?', callback_data='map')],
    [InlineKeyboardButton(text='Как нас найти?', callback_data='office')],
]