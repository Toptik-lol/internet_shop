import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, UserMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    picture = sqlalchemy.Column(sqlalchemy.String, default='../static/picture/product_default.png')
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    producer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    advantage = sqlalchemy.Column(sqlalchemy.String)