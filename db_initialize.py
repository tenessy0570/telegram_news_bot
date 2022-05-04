import asyncio

from db import config, actions
from db import models
from db.config import async_session


async def main():
    async with config.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

        async with async_session() as session:
            sources_actions = actions.NewsSourceAction(session)
            await sources_actions.create_source(name='bbc-news')
            await sources_actions.create_source(name='aftenposten')
            await sources_actions.create_source(name='bloomberg')
            await sources_actions.create_source(name='cnn')
asyncio.run(main())
