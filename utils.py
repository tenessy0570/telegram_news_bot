import json
from actions_logging import logging

import constants
from db import actions
from news.news_retriever import NewsApi


async def get_current_user(session, event):
    user_actions = actions.UserAction(session)
    return await user_actions.get_user_by_name(event.from_user.full_name)


async def change_n_value(session, event, n_value):
    """
    Changes user's N value
    """
    user_actions = actions.UserAction(session)
    if not n_value.isdigit():
        await event.answer('Wrong value type.')  # Do nothing if value has wrong type
        return None

    n_value = int(n_value)

    if not 1 <= n_value <= 10:
        await event.answer("N value should be 1 <= N <= 10")  # Do nothing if value is too high or too low
        return None

    current_user = await get_current_user(session, event)
    n_value_before_changing = current_user.value_n

    await user_actions.update_user(
        user_id=current_user.id,
        value_n=n_value
    )

    await event.answer(f"N value has been changed from {n_value_before_changing} to {n_value}")
    await logging.log_action(
        action_type=f'change N value from {n_value_before_changing} to {n_value}',
        user_id=current_user.id
    )


def get_decoded_json(json_body) -> dict:
    """
    Decodes json to python dictionary
    """
    decoder = json.decoder.JSONDecoder()
    decoded_json = decoder.decode(json_body)
    return decoded_json


def dict_to_string(entry_dict) -> str:
    result = '\n\n'.join(f'{key}:\n{entry_dict[key]}' for key in entry_dict)
    return result


async def get_source_by_name(session, source_name):
    sources_actions = actions.NewsSourceAction(session)
    source = await sources_actions.get_source_by_name(name=source_name)
    return source


async def set_user_source(event, session, source):
    current_user = await get_current_user(session, event)
    user_actions = actions.UserAction(session)
    await user_actions.update_user(user_id=current_user.id, selected_news_source=source.id)
    await event.answer(f"News source has been set to {source.name}")


def get_prettified_sources(sources):
    return '\n'.join((f'{index + 1}. {source.name}' for index, source in enumerate(sources)))


async def get_all_sources(session):
    sources_actions = actions.NewsSourceAction(session)
    sources = await sources_actions.get_all_sources()
    return sources


async def get_source_by_id(session, user):
    sources_actions = actions.NewsSourceAction(session)
    source = await sources_actions.get_source_by_id(user.selected_news_source)
    return source


async def send_news(user, source, event):
    news_retriever = NewsApi(user.value_n, source.name)
    news = await news_retriever.retrieve_news()
    await event.answer(dict_to_string(news), disable_web_page_preview=True)


async def send_start_message(event):
    await event.answer(constants.BOT_DESCRIPTION)


async def add_new_user(session, event):
    user_actions = actions.UserAction(session)
    await user_actions.create_user(name=event.from_user.full_name)
