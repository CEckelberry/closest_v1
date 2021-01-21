"""SQLAlchemy models for Closest."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """Users in the system"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.Text, nullable=False, unique=True)

    phone_number = db.Column(db.Text)

    image_url = db.Column(db.Text, default="/static/images/default-pic.png",)

    favorites = db.relationship("Favorite")

    @classmethod
    def signup(cls, username, password, email, phone_number, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
            phone_number=phone_number,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

         If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Favorite(db.Model):
    """favorite stops to save"""

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    description = db.Column(db.Text,)

    address = db.Column(db.Text, nullable=False)

    latitude = db.Column(db.Float,)

    longitude = db.Column(db.Float,)

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False,
    )

    user = db.relationship("User")


def connect_db(app):
    """Connection to app.py"""

    db.app = app
    db.init_app(app)
