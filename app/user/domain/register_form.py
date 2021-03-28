from flask_wtf import FlaskForm

from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    username = TextField(
        'username',
        validators=[DataRequired(), Length(min=2, max=25)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=2, max=25)]
    )