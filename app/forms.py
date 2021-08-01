from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Optional


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


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
