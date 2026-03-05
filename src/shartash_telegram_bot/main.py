import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from shartash_telegram_bot.handlers import router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def main():

    bot = Bot(token=TOKEN)

    dp = Dispatcher()

    dp.include_router(router)

    print("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())