from flask import Flask
from flask_login import LoginManager, login_user, login_required, logout_user
import db_manager
from models.book import Book
from models.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"


@app.route("/")
def main_page():
    session = db_manager.create_session()
    books = session.query(Book).all()
    print(books[0].author)
    print(books[0].user)

    users = session.query(User).all()
    print(users[0])
    print(users[0].added_books)
    print(users[0].downloaded_books)


if __name__ == "__main__":
    db_manager.db_init()

    # login_manager = LoginManager()
    # login_manager.init_app(app)

    # from models import user

    # @login_manager.user_loader
    # def load_user(user_id):
    #     session = db_manager.create_session()
    #     return session.query(user.User).get(user_id)


    app.run(host="localhost", port=8080)
