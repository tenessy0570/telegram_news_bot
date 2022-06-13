import asyncio

from db import config, models
from db.config import async_session
from db.db_managers import SourceManager


async def main():
    async with config.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

        async with async_session() as session:
            await SourceManager.create_source(session, name='bbc-news')
            await SourceManager.create_source(session, name='aftenposten')
            await SourceManager.create_source(session, name='bloomberg')
            await SourceManager.create_source(session, name='cnn')


if __name__ == '__main__':
    asyncio.run(main())
