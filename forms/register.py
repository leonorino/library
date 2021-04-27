from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, StopValidation
from models.user import User


def check_username(form, user_name):
    import db_manager
    session = db_manager.create_session()

    user = session.query(User).filter(User.name == user_name.data.strip()) \
        .first()
    if user:
        raise StopValidation("Пользователь с таким именем уже существует")


def check_password(form, password):
    repeated_password = form.password_again.data
    if password.data != repeated_password:
        raise StopValidation("Пароли не совпадают")


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), check_username])
    password = PasswordField('Пароль', validators=[DataRequired(), check_password])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
