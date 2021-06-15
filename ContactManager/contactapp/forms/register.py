from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from contactapp.models import User

class RegisterationForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired(), Length(min=2, max=20), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    subscribe = BooleanField('Subscribe')
    submit = SubmitField('Create')

    def validate_username(self, username):
        if self.password.data == "password":
            raise ValidationError('Password is week in user')
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_password(self, password):
        if(password.data == "password"):
            raise ValidationError('Password is week')

