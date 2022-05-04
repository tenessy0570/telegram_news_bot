import sqlalchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class NewsSource(Base):
    __tablename__ = 'news_sources'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.CHAR(length=255), nullable=False, unique=True)
    link = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)


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
    value_n = sqlalchemy.Column(sqlalchemy.Integer, default=5)
    join_date = sqlalchemy.Column(sqlalchemy.DATETIME, default=sqlalchemy.sql.func.now())


class Action(Base):
    __tablename__ = 'actions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    action_type = sqlalchemy.Column(sqlalchemy.CHAR(length=255), nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(User.id),
        nullable=False
    )
    used_news_source = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(NewsSource.id),
        nullable=True,
        default=None
    )
    datetime = sqlalchemy.Column(sqlalchemy.DATETIME, default=sqlalchemy.sql.func.now())
