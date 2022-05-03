import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from os import getenv

from db.config import async_session, engine, Base
from db.actions.user import UserAction

load_dotenv()
BOT_TOKEN = getenv('BOT_TOKEN')


async def start_handler(event: types.Message):
    await event.answer("you are " + event.from_user.full_name + "!")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await event.answer(Base.__subclasses__())


async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler, commands={"start", "restart"})
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())
