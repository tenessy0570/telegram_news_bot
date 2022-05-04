from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils import exceptions
from os import getenv
from sqlalchemy import exc

from db.config import async_session
from db import actions
from utils import change_n_value

load_dotenv()
BOT_TOKEN = getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def send_welcome(event: types.Message):
    await event.answer("Hello, " + event.from_user.full_name + "!")

    async with async_session() as session:
        user_actions = actions.UserAction(session)
        current_user = await user_actions.get_user_by_name(event.from_user.full_name)

        if not current_user:
            await event.answer('Adding new user to database...')
            await user_actions.create_user(name=event.from_user.full_name)


@dp.message_handler(commands=['update_n'])
async def get_users(event: types.Message):
    async with async_session() as session:

        try:
            n_value = event.get_args()
        except exceptions.MessageTextIsEmpty:
            await event.answer("Type number to set value.")
            return None

        await change_n_value(session, event, n_value)


if __name__ == '__main__':
    executor.start_polling(dp)
