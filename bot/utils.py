import json

import constants

from news.news_retriever import NewsApi


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


def get_prettified_sources(sources) -> str:
    return '\n'.join((f'{count}. {source.name}' for count, source in enumerate(sources, 1)))


async def send_news(user, source, event):
    news_retriever = NewsApi(user.value_n, source.name)
    news = await news_retriever.retrieve_news()
    await event.answer(dict_to_string(news), disable_web_page_preview=True)


async def send_start_message(event):
    await event.answer(constants.BOT_DESCRIPTION)
