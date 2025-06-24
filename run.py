import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN

from app.user import user
from app.admin import admin



async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(user)
    dp.include_routers(admin)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        pass