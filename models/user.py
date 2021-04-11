import sqlalchemy
from sqlalchemy import orm
from db_manager import database
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


user_to_book = sqlalchemy.Table(
    "user_to_book",
    database.metadata,
    sqlalchemy.Column("users", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("books", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("books.id"))
)


class User(database, UserMixin, SerializerMixin):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    added_books = orm.relationship("Book", backref="users")
    downloaded_books = orm.relationship("Book",
                                        secondary="user_to_book",
                                        backref="books")
    reviews = orm.relationship("Review", backref="users")
