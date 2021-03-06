from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddCategoryForm(FlaskForm):
    title = StringField('Название категории', validators=[DataRequired()])
    description = StringField('Описание категории')
    submit = SubmitField('Создать')
