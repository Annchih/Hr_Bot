from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def faq_keyboard(faqs):
    static_faq = [
        [InlineKeyboardButton(text='Где мы находимся?', callback_data='place')],
        [InlineKeyboardButton(text='Не смогли найти вход? Как нас найти?', callback_data='office')],
        [InlineKeyboardButton(text='Другой вопрос? Задать вопрос HR', callback_data='ask_hr')],
    ]


    for faq in faqs:
            static_faq.append([
                InlineKeyboardButton(
                    text=faq["question"], callback_data=f"faq_{faq['id']}"
                )
            ])

    return InlineKeyboardMarkup(inline_keyboard=static_faq)
