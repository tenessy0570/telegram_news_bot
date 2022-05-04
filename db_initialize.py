import asyncio

from db import config
from db import models


async def main():
    async with config.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

asyncio.run(main())
