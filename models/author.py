import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from ..db_manager import database


class Author(database):
    __tablename__ = "authors"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)

    books = orm.relation("Book", back_populates="author")
