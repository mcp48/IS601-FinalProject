from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email


class SignupForm(FlaskForm):
    """Sign up for a user account."""
    name = StringField(
        'Name',
        [DataRequired()]
    )
    email = StringField(
        "Email",
        [
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        "Password",
        [
            DataRequired(message="Please enter a password.")
        ]
    )
    confirmPassword = PasswordField(
        "Repeat Password",
        [
            EqualTo(password, message="Passwords must match.")
        ]
    )
    submit = SubmitField("Submit")