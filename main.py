from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from data.products import Product

from datetime import datetime
from os import path


from forms.user import RegisterForm, LoginForm, EditRegisterForm
from forms.product import ProductForm


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/shop.db")
    app.run()


@app.route("/")
def index():
    # db_sess = db_session.create_session()
    # jobs = db_sess.query(Jobs)
    return render_template("index.html", title='Lemon Shop')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", form=form, message="Такой пользователь уже есть")

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/users/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    form = EditRegisterForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()

        if user:
            form.surname.data = user.surname
            form.name.data = user.name
            form.email.data = user.email
            form.phone.data = user.phone
            form.address.data = user.address
            form.is_admin.data = user.is_admin
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()

        if user and (current_user.id == user.id or current_user.is_admin):
            user.surname = form.surname.data
            user.name = form.name.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.address = form.address.data
            if form.password.data:
                if form.password.data != form.password_again.data:
                    return render_template("register.html", form=form, message="Пароли не совпадают")
                else:
                    user.set_password(form.password.data)
            if current_user.is_admin:
                user.is_admin = form.is_admin.data

            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('register.html', title='Редактирование данных пользователя', form=form)


@app.route('/users')
@login_required
def users_list():
    if current_user.is_admin:
        db_sess = db_session.create_session()
        user_list = db_sess.query(User)
        return render_template("users.html", user_list=user_list)
    else:
        abort(404)
        return redirect('/')


@app.route('/user_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def user_delete(id):
    if current_user.is_admin:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        db_sess.delete(user)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/products', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = Product(title=form.title .data, description=form.description.data,
                          producer=form.producer.data, price=float(form.price.data), count=int(form.count.data),
                          advantage=form.advantage.data)
        if form.picture.data != '':
            f = form.picture.data
            parent_dir = path.dirname(path.abspath(__file__))
            basename = parent_dir + '\\static\\pictures\\pic'
            suffix = datetime.now().strftime("%y%m%d_%H%M%S")
            filename = "_".join([basename, suffix, '.png'])
            g = open(filename, 'wb')
            g.write(f.getbuffer())
            g.close()
            product.picture = filename
            print(form.picture.data)

        db_sess.add(product)
        db_sess.commit()
        return redirect('/')
    return render_template('product.html', title='Добавление товара', form=form)


if __name__ == '__main__':
    main()
