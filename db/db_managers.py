from sqlalchemy import update
from sqlalchemy.future import select

from db.models import Action, Source, User


class UserManager:
    @classmethod
    async def create_user(cls, session, name: str) -> None:
        new_user = User(name=name)
        session.add(new_user)
        await session.commit()

    @classmethod
    async def get_all_users(cls, session) -> list[User]:
        q = await session.execute(select(User).order_by(User.id))
        return q.scalars().all()

    @classmethod
    async def get_user_by_id(cls, session, user_id: int) -> User | None:
        q = await session.execute(select(User).where(User.id == user_id))
        try:
            return q.fetchone()[0]
        except TypeError:
            return None

    @classmethod
    async def get_user_by_name(cls, session, name: str) -> User | None:
        q = await session.execute(select(User).where(User.name == name))
        try:
            return q.fetchone()[0]
        except TypeError:
            return None

    @classmethod
    async def update_user(
            cls,
            session,
            user_id: int,
            selected_news_source: int = None,
            value_n: int = None
    ) -> None:
        q = update(User).where(User.id == user_id)
        if selected_news_source:
            q = q.values(selected_news_source=selected_news_source)
        if value_n:
            q = q.values(value_n=value_n)
        q.execution_options(synchronize_session="fetch")

        await session.execute(q)
        await session.commit()


class SourceManager:
    @classmethod
    async def create_source(cls, session, name: str) -> None:
        new_source = Source(name=name)
        session.add(new_source)
        await session.commit()

    @classmethod
    async def get_all_sources(cls, session) -> list[Source]:
        q = await session.execute(select(Source).order_by(Source.id))
        return q.scalars().all()

    @classmethod
    async def get_source_by_id(cls, session, source_id: int) -> Source | None:
        q = await session.execute(select(Source).where(Source.id == source_id))
        try:
            return q.fetchone()[0]
        except TypeError:
            return None

    @classmethod
    async def get_source_by_name(cls, session, name: str) -> Source | None:
        q = await session.execute(select(Source).where(Source.name == name))
        try:
            return q.fetchone()[0]
        except TypeError:
            return None


class ActionManager:
    @classmethod
    async def create_action(
            cls,
            session,
            action_type: str,
            user_id: int,
            used_news_source: int = None
    ) -> None:
        new_action = Action(
            action_type=action_type,
            user_id=user_id,
            used_news_source=used_news_source
        )

        session.add(new_action)
        await session.commit()
