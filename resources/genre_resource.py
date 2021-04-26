from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from db_manager import create_session
from models.genre import Genre


def abort_if_genre_not_found(genre_id):
    session = create_session()
    genre = session.query(Genre).get(genre_id)
    if not genre:
        abort(404, message=f"Жанра с id {genre_id} не существует")


class GenreResource(Resource):
    def get(self, genre_id):
        abort_if_genre_not_found(genre_id)
        session = create_session()
        genre = session.query(Genre).get(genre_id)
        genre_dict = genre.to_dict(rules=("-books",))
        return jsonify({'genre': genre_dict})
