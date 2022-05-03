import sqlalchemy

from db.config import Base


class NewsSource(Base):
    __tablename__ = 'news_sources'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.CHAR(length=255), nullable=False, unique=True)
    link = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
