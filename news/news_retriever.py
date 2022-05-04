from os import getenv
import aiohttp

from utils import get_decoded_json


class NewsRetriever:
    def __init__(self):
        pass

    async def retrieve_news(self):
        pass

    async def _retrieve_news(self):
        pass


class NewsApi(NewsRetriever):
    def __init__(self, page_size: int, source: str):
        super().__init__()
        self._source = source
        self._url = \
            f'https://newsapi.org/v2/top-headlines?sources={self._source}&' \
            f'apiKey={getenv("NEWSAPI_APIKEY")}&pageSize={page_size}'

    async def retrieve_news(self) -> dict:
        """
        Retrieves news headers based on page_size value (amount of headers)
        returns dictionary where key = title of new, value = it's url
        """

        return await self._retrieve_news()

    async def _retrieve_news(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as response:
                response_text = await response.text()
                decoded_json = get_decoded_json(response_text)
                articles = {article['title']: article['url'] for article in decoded_json['articles']}
                return articles
