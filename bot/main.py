from os import getenv

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from utils import get_prettified_sources, send_news, send_start_message

from actions_logging.logging import SQLiteLogger
from db.config import async_session
from db.utils import (add_new_user, change_n_value, get_all_sources,
                      get_current_user, get_source_by_name, get_user_source,
                      set_user_source)

load_dotenv()
BOT_TOKEN = getenv('BOT_TOKEN')
NEWSAPI_APIKEY = getenv('NEWSAPI_APIKEY')

if not BOT_TOKEN or not NEWSAPI_APIKEY:
    raise KeyError("Define BOT_TOKEN and NEWSAPI_APIKEY constants in .env file")

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
    await SQLiteLogger.log_action(
        session,
        action_type='command /start',
        event=event
    )


@dp.message_handler(commands=['help'])
async def provide_help(event: types.message):
    await send_start_message(event)

    async with async_session() as session:
        await SQLiteLogger.log_action(
            session,
            action_type='/help',
            event=event
        )


@dp.message_handler(commands=['update_n'])
async def update_n(event: types.Message):
    n_value = event.get_args()

    if not n_value:
        await event.answer("Type number to set value.")
        return None

    async with async_session() as session:
        await change_n_value(session, event, n_value)


@dp.message_handler(commands=['get_news'])
async def get_news(event: types.Message):
    async with async_session() as session:
        current_user = await get_current_user(session, event)
        user_source = await get_user_source(session, current_user)

        if not user_source:
            await event.answer('Choose source you want to get news from using /set_source <source>')
            return None

        await send_news(current_user, user_source, event)
        await SQLiteLogger.log_action(
            session,
            action_type='get news',
            user_id=current_user.id,
            used_news_source=user_source.name
        )


@dp.message_handler(commands=['get_sources'])
async def get_sources(event: types.Message):
    async with async_session() as session:
        sources = await get_all_sources(session)

        prettified_sources = get_prettified_sources(sources)
        await event.answer(prettified_sources)
        await SQLiteLogger.log_action(
            session,
            action_type='get sources list',
            event=event
        )


@dp.message_handler(commands=['set_source'])
async def set_source(event: types.Message):
    source_name = event.get_args().lower()

    async with async_session() as session:
        source = await get_source_by_name(session, source_name)

        if not source:
            await event.answer('Type name of source after /set_source command '
                               'to set your preferrable news source')
            return None

        await set_user_source(event, session, source)
        await SQLiteLogger.log_action(
            session,
            action_type='set source',
            event=event,
            used_news_source=source.name
        )


if __name__ == '__main__':
    executor.start_polling(dp)
