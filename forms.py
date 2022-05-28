from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    profile_pic = StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserEditForm(FlaskForm):
    """Form for editing user profile"""

    username = StringField('Username', validators=[DataRequired()])
    name = StringField('(optional) Name')
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_pic = StringField('(Optional) Image URL')
    bio = TextAreaField('(Optional) Write a bit about your recipe page')
    fav_spices = StringField('(Optional) Favorite Spices')
    fav_appliances = StringField('(Optional) Favorite Appliances')
    fav_cuisine = StringField('(Optional) Favorite Cuisine')
    password = PasswordField('Password', validators=[Length(min=6)])