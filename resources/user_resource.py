from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from db_manager import create_session
from models.user import User
from werkzeug.security import generate_password_hash
from .parsers import user_parser


def abort_if_user_not_found(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        user_dict = user.to_dict(only=('name',))
        user_dict["added_books"] = [book.title for book in user.added_books]

        return jsonify({'users': user_dict})


class UserListResource(Resource):
    def get(self):
        session = create_session()
        users = session.query(User).all()
        return jsonify({'users': [user.to_dict(
            only=('name', )) for user in users]})

    def post(self):
        args = user_parser.parse_args()
        session = create_session()
        user = User(
            name=args['name'],
            hashed_password=generate_password_hash(args['hashed_password'])
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
