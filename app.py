import os
import uuid
from flask import Flask, render_template, redirect, request, url_for, send_file, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user

import db_manager
from models.book import Book
from models.author import Author
from models.genre import Genre
from models.review import Review
from forms.add_book import AddBookForm
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.add_review import AddReviewForm
from flask_restful import Api

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['JSON_AS_ASCII'] = False


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def redirect_to_main():
    return redirect("/books")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_manager.create_session()
        user = db_sess.query(User).filter(
            User.name == form.name.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title="Авторизация",
                               message="Неверное имя или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_manager.create_session()

        existing_user = session.query(User) \
            .filter(User.name == form.name.data).first()

        if existing_user:
            return render_template("register.html", title="Регистрация",
                                   message="Пользователь уже существует",
                                   form=form)

        if form.password.data != form.password_again.data:
            return render_template("register.html", title="Регистрация",
                                   message="Пароли не совпадают", form=form)

        new_user = User()
        new_user.name = form.name.data
        new_user.set_password(form.password.data)

        session.add(new_user)
        session.commit()
        login_user(new_user, remember=False)
        return redirect("/")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/books", methods=["GET", "POST"])
def show_main_page():
    session = db_manager.create_session()
    if request.method == "GET":
        books = session.query(Book).all()
        print(type(books[0].reviews[0].date_added))
        return render_template("book_list.html", books=books,
                               title="Список книг")
    elif request.method == "POST":
        return redirect(url_for("show_search_results",
                                search_by=request.form['type'],
                                value=request.form['search_query']))


@app.route("/books/search/?search_by=<search_by>&value=<value>",
           methods=["GET", "POST"])
def show_search_results(search_by, value):
    if request.method == "GET":
        session = db_manager.create_session()

        if search_by == "title":
            books = session.query(Book).filter(Book.title.like(f"%{value}%")) \
                .all()
            return render_template("book_list.html", books=books,
                                   title="Список книг")
        elif search_by == "author":
            authors = session.query(Author).filter(Author.name
                                                   .like(f"%{value}%"))
            all_books = list()
            for author in authors:
                books = session.query(Book).filter(Book.author_id ==
                                                   author.id).all()
                all_books += books

            return render_template("book_list.html", books=all_books,
                                   title="Список книг")
    elif request.method == "POST":
        return redirect(url_for("show_search_results",
                                search_by=request.form['type'],
                                value=request.form['search_query']))


@app.route("/books/id=<int:book_id>/reviews/add", methods=["GET", "POST"])
def show_review_add_page(book_id):
    session = db_manager.create_session()
    book = session.query(Book).get(book_id)

    form = AddReviewForm()
    if form.validate_on_submit():
        user = current_user
        new_review = Review(rating=form.rating.data, content=form.content.data,
                            book_id=book_id, user_id=user.id)
        session.add(new_review)
        session.commit()
        return redirect(f"/books/id={book_id}/reviews")
    return render_template("add_review.html", form=form, book=book)


@app.route("/books/id=<int:book_id>/reviews", methods=["GET", "POST"])
def show_reviews_page(book_id):
    session = db_manager.create_session()
    book = session.query(Book).get(book_id)

    reviews = book.reviews
    return render_template("review_list.html", book=book)


@login_required
@app.route("/books/add", methods=["GET", "POST"])
def show_book_add_page():
    form = AddBookForm()

    if form.validate_on_submit():
        try:
            session = db_manager.create_session()

            new_book = Book(
                title=form.title.data,
                description=form.description.data,
                added_by=current_user.id
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

            request.files['cover'].save(os.path.join(
                content_directory, "cover").replace("\\", "/"))
            request.files['fb2_file'].save(os.path.join(
                content_directory, "book.fb2").replace("\\", "/"))
            request.files['epub_file'].save(os.path.join(
                content_directory, "book.epub").replace("\\", "/"))

            session.add(new_book)
            session.commit()

            return redirect("/")
        except Exception:
            return render_template('error.html')

    return render_template("add_book.html", title="Добавление книги", form=form)


@app.route("/books/id=<int:book_id>/get/<format>")
def send_book(book_id, format):
    session = db_manager.create_session()
    book = session.query(Book).get(book_id)
    data_folder = book.data_folder
    book.downloads_count += 1
    session.add(book)
    session.commit()
    return send_file(f"{data_folder}/book.{format}",
                     attachment_filename=f"book.{format}", as_attachment=True)


@app.route("/books/id=<int:book_id>/reviews")
def show_reviews(book_id):
    session = db_manager.create_session()
    book = session.query(Book).get(book_id)
    print(type(book.reviews[0].date_added))
    return render_template("review_list.html", book=book)


@app.route("/user_profile")
def show_user_profile():
    user = current_user
    return render_template("profile.html", user=user)


if __name__ == "__main__":
    db_manager.db_init()

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models.user import User


    @login_manager.user_loader
    def load_user(user_id):
        session = db_manager.create_session()
        return session.query(User).get(user_id)


    api = Api(app)
    from resources.user_resource import UserResource, UserListResource
    from resources.book_resource import BookResource, BookListResource
    from resources.genre_resource import GenreResource
    from resources.genre_resource import GenreListResource
    from resources.author_resource import AuthorResource
    from resources.author_resource import AuthorListResource

    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(UserListResource, '/api/users')
    api.add_resource(BookResource, "/api/books/<int:book_id>")
    api.add_resource(BookListResource, "/api/books")
    api.add_resource(GenreResource, "/api/genres/<int:genre_id>")
    api.add_resource(GenreListResource, "/api/genres")
    api.add_resource(AuthorResource, "/api/authors/<int:author_id>")
    api.add_resource(AuthorListResource, "/api/authors")
    app.run(host="localhost", port=8080, debug=True)
