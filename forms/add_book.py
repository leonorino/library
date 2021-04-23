from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, FileField
from wtforms import SelectField
from wtforms.validators import DataRequired, ValidationError

from models.book import Book


def validate_book_name(form, book_title):
    import db_manager
    session = db_manager.create_session()

    book = session.query(Book).filter(Book.title == book_title.data.strip()) \
        .first()

    if book:
        raise ValidationError("Книга с таким названием уже существует")


class AddBookForm(FlaskForm):
    title = StringField("Название книги",
                        validators=[DataRequired(), validate_book_name])
    description = StringField("Описание", validators=[DataRequired()])
    author = StringField("Автор", validators=[DataRequired()])
    genre = StringField("Жанр", validators=[DataRequired()])
    cover = FileField("Обложка", validators=[DataRequired()])
    epub_file = FileField("Книга в формате epub", validators=[DataRequired()])
    fb2_file = FileField("Книга в формате fb2", validators=[DataRequired()])
    submit = SubmitField("Добавить")
