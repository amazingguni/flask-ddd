from flask_wtf import FlaskForm

from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = TextField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
