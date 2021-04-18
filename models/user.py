import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from db_manager import database
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

user_to_book = sqlalchemy.Table(
    "user_to_book",
    database.metadata,
    sqlalchemy.Column("user", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("book", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("books.id"))
)


class User(database, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    reviews = orm.relationship("Review", back_populates="user")
    added_books = orm.relationship("Book", back_populates="user")
    downloaded_books = orm.relationship("Book", secondary="user_to_book",
                                        backref="users")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
