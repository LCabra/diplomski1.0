from flask_login import UserMixin
from website import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def get_id(self):
        return str(self.user_id)

class Pitch(db.Model):
    __tablename__ = 'pitches'

    pitch_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    dimensions = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200))
