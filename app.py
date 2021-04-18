import os
import uuid
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user

import db_manager
from models.book import Book
from models.user import User
from models.author import Author
from models.genre import Genre
from forms.add_book import AddBookForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"


@app.route("/")
def redirect_to_main():
    return redirect("/books/add")


@app.route("/books/add", methods=["GET", "POST"])
def show_main_page():
    form = AddBookForm()

    if form.validate_on_submit():
        print("Validated")
        session = db_manager.create_session()

        new_book = Book(
            title=form.title.data,
            description=form.description.data,
            added_by=1
        )

        existing_author = session.query(Author) \
            .filter(Author.name == form.author.data.strip()).first()
        if existing_author:
            new_book.author = existing_author.id
        else:
            new_author = Author(name=form.author.data.strip())
            session.add(new_author)
            session.flush()
            new_book.author = new_author

        existing_genre = session.query(Genre) \
            .filter(Genre.name == form.genre.data.strip()).first()
        if existing_genre:
            new_book.genre = existing_genre.id
        else:
            new_genre = Genre(name=form.genre.data.strip())
            session.add(new_genre)
            session.flush()
            new_book.genre = new_genre

        directory_names = os.listdir("static/books")
        new_directory_name = str(uuid.uuid4())
        while new_directory_name in directory_names:
            new_directory_name = str(uuid.uuid4())

        os.mkdir(os.path.join("static/books", new_directory_name))
        new_book.data_folder = os.path.join("static/books",
            new_directory_name).replace("\\", "/")

        content_directory = os.path.join("static/books", new_directory_name)

        request.files['cover'].save(os.path.join(content_directory,
            "cover.png").replace("\\", "/"))
        request.files['fb2_file'].save(os.path.join(content_directory,
            "book.fb2").replace("\\", "/"))
        request.files['epub_file'].save(os.path.join(content_directory,
            "book.epub").replace("\\", "/"))

        session.add(new_book)
        session.commit()

    return render_template("add_book.html", title="Добавление книги", form=form)


if __name__ == "__main__":
    db_manager.db_init()

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        session = db_manager.create_session()
        return session.query(User).get(user_id)


    app.run(host="localhost", port=8080, debug=True)
