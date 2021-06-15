from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError

class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20), Email()])
    profile_picture = FileField('Change your profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')