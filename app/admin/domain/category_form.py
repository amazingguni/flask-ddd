from flask_wtf import FlaskForm

from wtforms import TextField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    name = TextField(
        'name',
        validators=[DataRequired(), Length(min=2, max=25)]
    )
