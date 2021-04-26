from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from db_manager import create_session
from models.author import Author


def abort_if_author_not_found(author_id):
    session = create_session()
    author = session.query(Author).get(author_id)
    if not author:
        abort(404, message=f"Автора с id {author_id} не существует")


class AuthorResource(Resource):
    def get(self, author_id):
        abort_if_author_not_found(author_id)
        session = create_session()
        author = session.query(Author).get(author_id)
        author_dict = author.to_dict(rules=("-books",))
        return jsonify({'author': author_dict})


class AuthorListResource(Resource):
    def get(self):
        session = create_session()
        authors = session.query(Author).all()
        return jsonify({
            'authors': [author.to_dict(rules=("-books",))
                        for author in authors]
        })
