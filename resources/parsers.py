from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', required=True)
user_parser.add_argument('hashed_password', required=True)
