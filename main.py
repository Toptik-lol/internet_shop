from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.users import User

from forms.user import RegisterForm, LoginForm


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/shop.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('base.html', title='Добавление работы')


if __name__ == '__main__':
    main()
