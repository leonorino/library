import sqlalchemy
from datetime import datetime
from db_manager import database
from sqlalchemy_serializer import SerializerMixin


class Review(database, SerializerMixin):
    __tablename__ = "reviews"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id"))
    date_added = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now)