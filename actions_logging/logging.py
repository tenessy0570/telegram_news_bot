from abc import ABC, abstractmethod

from db.db_managers import ActionManager, UserManager


class Logger(ABC):
    @classmethod
    @abstractmethod
    async def log_action(
            cls,
            session,
            action_type: str,
            user_id: int = None,
            event=None,
            used_news_source: int = None
    ) -> None:
        pass


class SQLiteLogger(Logger):
    @classmethod
    async def log_action(
            cls,
            session,
            action_type: str,
            user_id: int = None,
            event=None,
            used_news_source: int = None
    ) -> None:

        if not user_id and not event:
            raise UserWarning("Either user_id or event argument should be passed to method.")

        if event:
            user = await UserManager.get_user_by_name(session, event.from_user.full_name)
            user_id = user.id

        await ActionManager.create_action(
            session,
            action_type=action_type,
            user_id=user_id,
            used_news_source=used_news_source
        )
