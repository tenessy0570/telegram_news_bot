import json
from os import getenv
from abc import ABC

import aiohttp

Title = str
Url = str


class NewsRetriever(ABC):
    async def retrieve_news(self):
        pass


class NewsApi(NewsRetriever):
    def __init__(self, page_size: int, source: str):
        super().__init__()
        self._source = source
        self._url = \
            f'https://newsapi.org/v2/top-headlines?sources={self._source}&' \
            f'apiKey={getenv("NEWSAPI_APIKEY")}&pageSize={page_size}'
        # Retrieving newsapi apikey from .env directly in f string is a way to avoid bug.

    async def retrieve_news(self) -> dict[Title, Url]:
        """
        Retrieves news headers based on page_size value (amount of headers)
        returns dictionary where key = title of new, value = it's url
        """

        return await self._retrieve_news()

    async def _retrieve_news(self) -> dict[Title, Url]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as response:
                response_text = await response.text()
                decoder = json.decoder.JSONDecoder()
                decoded_json = decoder.decode(response_text)
                articles = {article['title']: article['url'] for article in decoded_json['articles']}
                return articles
