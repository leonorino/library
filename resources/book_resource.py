from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from db_models import create_session
from models.book import Book


def abort_if_book_not_found(book_id):
    session = create_session()
    book = session.query(Book).get(book_id)
    if not book:
        abort(404, message=f"Книга с id {user_id} не существует")


class BookResource(Resource):
    def get(self, book_id):
        abort_if_book_not_found(book_id)
        session = create_session()
        book = session.query(Book).get(book_id)
        book_dict = book.to_dict(rules="-reviews,-author,-user,-genre")
        return jsonify({'book': book_dict})


class BookListResource(Resource):
    def get(self):
        session = create_session()
        books = session.query(Book).all()
        return jsonify({
            'books': [book.to_dict(rules="-reviews,-author,-user,-genre")
                      for book in books]
        })
