
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


def connect_db(app):
    """connect to database."""
    db.app = app
    db.init_app(app)


"""Models for Blogly."""


class User(db.Model):
    """User."""

    __tablename__ = "app_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False, unique=False)
    last_name = db.Column(db.String, nullable=False, unique=False)
    image_url = db.Column(db.String, nullable=False, unique=False,
                          default="https://goodshepherdrangeley.org/about-us/parish-leadership/no-image-icon-hi/")


class Post(db.Model):
    """User Post"""

    __tablename__ = "user_posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False, unique=False)
    content = db.Column(db.String, nullable=False, unique=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey(
        'app_users.id', ondelete="CASCADE"), )
