from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class BookForm(FlaskForm):
    book_name = StringField('Enter Book Name', validators=[DataRequired(), Length(min=1, max=100)])
    book_author = StringField('Enter Book Author', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Create Book')