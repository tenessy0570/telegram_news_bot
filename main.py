from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils import exceptions
from os import getenv

from db.config import async_session
from utils import (
    change_n_value,
    get_current_user,
    get_source_by_name,
    set_user_source,
    get_prettified_sources,
    get_all_sources,
    get_source_by_id,
    send_news,
    send_start_message,
    add_new_user
)

load_dotenv()
BOT_TOKEN = getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start(event: types.Message):
    await event.answer("Hello, " + event.from_user.full_name + "!")

    async with async_session() as session:
        current_user = await get_current_user(session, event)

        if not current_user:
            await add_new_user(session, event)

    await send_start_message(event)


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
        user_source = await get_source_by_id(session, current_user)

    if not user_source:
        await event.answer('Choose source you want to get news from using /set_source <source>')
        return None

    await send_news(current_user, user_source, event)


@dp.message_handler(commands=['get_sources'])
async def get_sources(event: types.Message):
    async with async_session() as session:
        sources = await get_all_sources(session)

    prettified_sources = get_prettified_sources(sources)
    await event.answer(prettified_sources)


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
