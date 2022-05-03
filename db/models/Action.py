import sqlalchemy

from db.models.User import User
from db.models.NewsSource import NewsSource
from db.config import Base


class Action(Base):
    __tablename__ = 'actions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    action_type = sqlalchemy.Column(sqlalchemy.CHAR(length=255), nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(User.id),
        nullable=False
    ),
    used_news_source = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(NewsSource.id),
        nullable=True,
        default=None
    )
    datetime = sqlalchemy.Column(sqlalchemy.DATETIME, default=sqlalchemy.sql.func.now())
