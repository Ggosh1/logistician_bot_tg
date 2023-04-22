import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    tg_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    feedback = sqlalchemy.Column(sqlalchemy.Integer, default=None)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)