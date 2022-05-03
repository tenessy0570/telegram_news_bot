from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models.User import User


class UserAction:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, name: str):
        new_book = User(name=name)
        self.db_session.add(new_book)
        await self.db_session.flush()

    async def get_all_users(self) -> List[User]:
        q = await self.db_session.execute(select(User).order_by(User.id))
        return q.scalars().all()

    async def update_user(self, user_id: int, name: Optional[str], selected_news_source: Optional[int]):
        q = update(User).where(User.id == user_id)
        if name:
            q = q.values(name=name)
        if selected_news_source:
            q = q.values(selected_news_source=selected_news_source)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
