import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'product'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date_purchase = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    name_product = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price_product = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relation('User')
