from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, StopValidation
from models.user import User


def check_username(form, user_name):
    import db_manager

    session = db_manager.create_session()
    existing_user = session.query(User).filter(User.name == user_name.data.strip()).first()
    if not existing_user:
        raise StopValidation("Пользователя с таким именем не существует")


class LoginForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), check_username])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
