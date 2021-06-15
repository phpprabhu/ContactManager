from contactapp import db
from datetime import datetime
from contactapp import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    profile_image = db.Column(db.String(100), unique=False, nullable=False, default='default.jpg')

    books = db.relationship('Book', backref='books_added', lazy=True)

    def __repr__(self):
        return f'User Object display - {self.username}'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), unique=False, nullable=False)
    received_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='who_added', lazy=True)

    def __repr__(self):
        return f'Book Object {self.name}'
