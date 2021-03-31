from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Логин/почта', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class EditRegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Логин/почта', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    is_admin = BooleanField('Права администратора')
    submit = SubmitField('Применить')