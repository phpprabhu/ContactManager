from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WyevSgnSW7'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///contacts.db"
app.config['REMEMBER_COOKIE_NAME'] = 'contactCookie'
app.config['REMEMBER_COOKIE_DURATION'] = 1
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please login vennai"
login_manager.login_message_category = "danger"

from contactapp import routes






