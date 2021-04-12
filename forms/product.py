from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DecimalField, FileField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField('Название товара', validators=[DataRequired()])
    picture = FileField('Изображение')
    description = StringField('Описание товара', validators=[DataRequired()])
    category = StringField('Категория')
    producer = StringField('Производитель', validators=[DataRequired()])
    price = DecimalField('Цена', validators=[DataRequired()])
    count = DecimalField('Количество', places=0)
    advantage = StringField('Преимущества покупки товара')
    submit = SubmitField('Добавить')
