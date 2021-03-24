from flask import Flask

from data import db_session

from forms.user import RegisterForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/shop.db")
    app.run()


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    pass


if __name__ == '__main__':
    main()
