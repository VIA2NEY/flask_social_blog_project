from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    password_hash = sa.Column(sa.String(256), nullable=False)

    posts = so.relationship('Post', back_populates='author')

    def __repr__(self):
        return '<User %r>' % self.username
    

class Post(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    body = sa.Column(sa.String(140), nullable=False)
    timestamp = sa.Column(sa.DateTime, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'), nullable=False)

    author = so.relationship('User', back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)