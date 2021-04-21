from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class AddReviewForm(FlaskForm):
    rating = IntegerField("Оценка от 1 до 10", validators=[DataRequired(), NumberRange(1, 10)])
    content = StringField("Отзыв", validators=[DataRequired()])
    submit = SubmitField("Оставить отзыв")
