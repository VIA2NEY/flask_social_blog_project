from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from datetime import datetime


class User(UserMixin, db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    password_hash = sa.Column(sa.String(256), nullable=False)
    about_me = sa.Column(sa.String(140))
    last_seen = sa.Column(sa.DateTime, nullable=True, default= lambda: datetime.utcnow())

    posts = so.relationship('Post', back_populates='author')

    def __repr__(self):
        return '<User %r>' % self.username
    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    

class Post(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    body = sa.Column(sa.String(140), nullable=False)
    timestamp = sa.Column(sa.DateTime, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)

    author = so.relationship('User', back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)