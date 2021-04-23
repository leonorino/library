from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from db_manager import database


class Book(database, SerializerMixin):
    __tablename__ = "books"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("authors.id"))
    added_by = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("users.id"))
    genre_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("genres.id"))
    date_added = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False,
                                   default=datetime.now)
    data_folder = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    downloads_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False,
                                        default=0)

    reviews = orm.relationship("Review", back_populates="book")
    author = orm.relationship("Author")
    user = orm.relationship("User")
    genre = orm.relationship("Genre")
