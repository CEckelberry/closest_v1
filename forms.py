from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, URL


class AddFavoriteForm(FlaskForm):
    """Form for adding a favorite transit stop"""

    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description")
    address = StringField("Address", validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[Length(min=6, message="Password must be at least 6 characters")],
    )
    email = StringField("E-mail", validators=[DataRequired(), Email(),],)
    phone_number = StringField("(Optional) Phone_Number")
    image_url = StringField("(Optional) Image URL")


class EditUserForm(FlaskForm):
    """Form for editing users"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[Length(min=6, message="Password must be at least 6 characters")],
    )
    email = StringField("E-mail", validators=[DataRequired(), Email(),],)
    phone_number = StringField("(Optional) Phone_Number")
    image_url = StringField("(Optional) Image URL",)


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[Length(min=6, message="Password must be at least 6 characters")],
    )


class SearchForm(FlaskForm):
    """Search Form"""

    address = StringField("Address", validators=[DataRequired()])
