from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from ..db_manager import database


class Book(database, SerializerMixin):
    __tablename__ = "books"
    id = sqlalchemy.Column(sqlalchemy.Integer, primery_key=True, autoincrement=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("authors.id"))
    added_by = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    date_added = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now)
    cover = sqlalchemy.Column(sqlalchemy.String, nullable=False, default="/static/img/no_cover.jpg")
    data_folder = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    downloads_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    downloaded_by = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    genre = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"))
    reviews = sqlalchemy.orm.relationship("Review", backref="books")
    # user = orm.relation("User")
