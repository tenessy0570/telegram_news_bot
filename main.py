import json

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils import exceptions
from os import getenv
from sqlalchemy import exc

import constants
from news.news_retriever import NewsRetriever
from db.config import async_session
from db import actions
from utils import change_n_value, get_current_user, dict_to_string

load_dotenv()
BOT_TOKEN = getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start(event: types.Message):
    await event.answer("Hello, " + event.from_user.full_name + "!")

    async with async_session() as session:
        user_actions = actions.UserAction(session)
        current_user = await get_current_user(session, event)

        if not current_user:
            await user_actions.create_user(name=event.from_user.full_name)  # Add new user to database

    await event.answer(constants.BOT_DESCRIPTION)


@dp.message_handler(commands=['update_n'])
async def update_n(event: types.Message):
    async with async_session() as session:

        try:
            n_value = event.get_args()
        except exceptions.MessageTextIsEmpty:
            await event.answer("Type number to set value.")
            return None

        await change_n_value(session, event, n_value)


@dp.message_handler(commands=['get_news'])
async def get_news(event: types.Message):
    async with async_session() as session:
        current_user = await get_current_user(session, event)

    news_retriever = NewsRetriever(current_user.value_n)
    news = await news_retriever.retrieve_news()
    await event.answer(dict_to_string(news), disable_web_page_preview=True)

if __name__ == '__main__':
    executor.start_polling(dp)
