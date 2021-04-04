import sqlalchemy
from flask_login import UserMixin
# from flask_image_alchemy.storages import S3Storage
# from flask_image_alchemy.fields import StdImageField

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, UserMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    picture = sqlalchemy.Column(sqlalchemy.String, default='../static/picture/product_default.png')
    # picture = sqlalchemy.Column(StdImageField(storage=S3Storage(),
    #                                           variations={'thumbnail': {"width": 360, "height": 360, "crop": True}}),
    #                             nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    producer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    advantage = sqlalchemy.Column(sqlalchemy.String)
