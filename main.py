from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils import exceptions
from os import getenv

import constants
from news.news_retriever import NewsApi
from db.config import async_session
from db import actions
from utils import change_n_value, get_current_user, dict_to_string, get_source_by_name, set_user_source

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
        sources_actions = actions.NewsSourceAction(session)
        user_source = await sources_actions.get_source_by_id(current_user.selected_news_source)

    if not user_source:
        await event.answer('Choose source you want to get news from using /set_source <source>')
        return None

    news_retriever = NewsApi(current_user.value_n, user_source.name)
    news = await news_retriever.retrieve_news()
    await event.answer(dict_to_string(news), disable_web_page_preview=True)


@dp.message_handler(commands=['get_sources'])
async def get_sources(event: types.Message):
    async with async_session() as session:
        sources_actions = actions.NewsSourceAction(session)
        sources = await sources_actions.get_all_sources()

    sources_prettified = '\n'.join((f'{index + 1}. {source.name}' for index, source in enumerate(sources)))
    await event.answer(sources_prettified)
    await event.answer('awd')


@dp.message_handler(commands=['set_source'])
async def set_source(event: types.Message):
    source_name = event.get_args().lower()

    async with async_session() as session:
        source = await get_source_by_name(source_name)

        if not source:
            await event.answer('This source doesn\'t exist.')
            return None

        await set_user_source(event, session, source)


if __name__ == '__main__':
    executor.start_polling(dp)


