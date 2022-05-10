from typing import List

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models import *


class UserManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, name: str):
        new_user = User(name=name)
        self.db_session.add(new_user)
        await self.db_session.commit()

    async def get_all_users(self) -> List[User]:
        q = await self.db_session.execute(select(User).order_by(User.id))
        return q.scalars().all()

    async def get_user_by_id(self, user_id: int):
        q = await self.db_session.execute(select(User).where(User.id == user_id))
        try:
            return q.fetchone()[0]
        except TypeError:
            return None

    async def get_user_by_name(self, name: str):
        q = await self.db_session.execute(select(User).where(User.name == name))
        try:
            return q.fetchone()[0]
        except TypeError:
            return None

    async def update_user(
            self, user_id: int,
            selected_news_source: int = None,
            value_n: int = None
    ):
        q = update(User).where(User.id == user_id)
        if selected_news_source:
            q = q.values(selected_news_source=selected_news_source)
        if value_n:
            q = q.values(value_n=value_n)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
        await self.db_session.commit()


class NewsSourceManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_source(self, name: str):
        new_source = NewsSource(name=name)
        self.db_session.add(new_source)
        await self.db_session.commit()

    async def get_all_sources(self) -> List[NewsSource]:
        q = await self.db_session.execute(select(NewsSource).order_by(NewsSource.id))
        return q.scalars().all()

    async def get_source_by_id(self, source_id: int):
        q = await self.db_session.execute(select(NewsSource).where(NewsSource.id == source_id))
        try:
            return q.fetchone()[0]
        except TypeError:
            return None

    async def get_source_by_name(self, name: str):
        q = await self.db_session.execute(select(NewsSource).where(NewsSource.name == name))
        try:
            return q.fetchone()[0]
        except TypeError:
            return None


class ActionManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_action(self, action_type: str, user_id: int, used_news_source: int = None):
        new_action = Action(action_type=action_type, user_id=user_id, used_news_source=used_news_source)
        self.db_session.add(new_action)
        await self.db_session.commit()
