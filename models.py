from flask_sqlalchemy import SQLAlchemy

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
