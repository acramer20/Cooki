from datetime import datetime
from enum import unique

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    name = db.Column(db.Text)
    fav_cuisine = db.Column(db.Text)
    fav_appliances = db.Column(db.Text)
    fav_spices = db.Column(db.Text)
    profile_pic = db.Column(db.Text, default="https://dbdzm869oupei.cloudfront.net/img/vinylrugs/preview/39237.png")
    bio = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)


    @classmethod
    def signup(cls, username, email, password, profile_pic):
        """Signing up the user here
        
        Also will hash the password and adds user to system
        """
        hashed_pass = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password=hashed_pass,
            profile_pic=profile_pic
        )
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with the given 'username' and 'password'.
        if it cannot find the user or the password is incorrect, it returns False. 
        """
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Recipe(db.Model):
    """Each individual Recipe."""

    __tablename__ = 'recipes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    title = db.Column(
        db.Text,
        nullable=False,
    )

    recipe_img = db.Column(
        db.Text,
        nullable=False
    )

    user = db.relationship('User')


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

