from os import getenv

import aiohttp

from utils import get_decoded_json


class NewsRetriever:
    def __init__(self, page_size: int):
        self._url = \
            f'https://newsapi.org/v2/top-headlines?country=us&apiKey={getenv("NEWSAPI_APIKEY")}&pageSize={page_size}'

    async def retrieve_news(self) -> dict:
        """
        Retrieves news headers based on page_size value (amount of headers)
        """

        return await self._retrieve_news()

    async def _retrieve_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as response:
                response_text = await response.text()
                decoded_json = get_decoded_json(response_text)
                articles = {article['title']: article['url'] for article in decoded_json['articles']}
                return articles

    def get_url(self):
        return self._url
