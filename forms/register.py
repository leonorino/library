from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError
from models.user import User


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')