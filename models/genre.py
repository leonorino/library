import sqlalchemy
from sqlalchemy import orm
from db_manager import database
from sqlalchemy_serializer import SerializerMixin


class Genre(database, SerializerMixin):
    __tablename__ = "genres"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    books = orm.relationship("Book", back_populates="genre")
