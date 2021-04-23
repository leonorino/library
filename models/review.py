from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from db_manager import database


class Review(database, SerializerMixin):
    __tablename__ = "reviews"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    book_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("books.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey("users.id"))
    date_added = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now,
                                   nullable=False)

    user = orm.relationship("User")
    book = orm.relationship("Book")
