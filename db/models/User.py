import sqlalchemy

from db.models.NewsSource import NewsSource
from db.config import Base


class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.CHAR(length=255), nullable=False, unique=True)
    selected_news_source = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(NewsSource.id),
        nullable=True,
        default=None
    )
    joined_date = sqlalchemy.Column(sqlalchemy.DATETIME, default=sqlalchemy.sql.func.now())
