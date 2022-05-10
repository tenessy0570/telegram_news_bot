from abc import ABC

import db.db_managers
from db.config import async_session
from utils import get_current_user


class Logger(ABC):
    @staticmethod
    async def log_action(action_type: str, user_id: int = None, event=None, used_news_source: int = None) -> None:
        pass


class SQLiteLogger(Logger):
    @staticmethod
    async def log_action(action_type: str, user_id: int = None, event=None, used_news_source: int = None) -> None:
        async with async_session() as session:

            if not user_id and not event:
                raise UserWarning("Either user_id or event argument should be passed to method.")

            logging_actions = db.db_managers.ActionManager(session)

            if event:
                user = await get_current_user(session, event)
                user_id = user.id

            await logging_actions.create_action(
                action_type=action_type,
                user_id=user_id,
                used_news_source=used_news_source
            )
