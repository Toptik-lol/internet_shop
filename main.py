from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from data.products import Product
from data.categorys import Category
from data.baskets import Basket

from datetime import datetime
from os import path


from forms.user import RegisterForm, LoginForm, EditRegisterForm
from forms.product import ProductForm
from forms.add_category import AddCategoryForm


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/shop.db")
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    products = db_sess.query(Product)
    categories = db_sess.query(Category)
    return render_template("index.html", title='Lemon Shop', products=products, categories=categories, null=-1)


@app.route("/<int:id>")
def index_id(id):
    db_sess = db_session.create_session()
    products = db_sess.query(Product).filter(Product.category == id).all()
    categories = db_sess.query(Category)
    return render_template("index.html", title='Lemon Shop', products=products, categories=categories, null=-1)


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
    db_sess = db_session.create_session()
    categories = db_sess.query(Category)
    category_flag = 'None'
    if form.validate_on_submit():
        product = Product(title=form.title.data, description=form.description.data,
                          producer=form.producer.data, price=float(form.price.data), count=int(form.count.data),
                          advantage=form.advantage.data)
        if form.picture.data:
            f = form.picture.data
            parent_dir = path.dirname(path.abspath(__file__))
            basename = parent_dir + '\\static\\pictures\\pic'
            suffix = datetime.now().strftime("%y%m%d_%H%M%S")
            filename = "_".join([basename, suffix, '.png'])
            g = open(filename, 'wb')
            g.write(f.getbuffer())
            g.close()
            product.picture = '/static/pictures/pic_' + suffix + '_.png'

        cat = db_sess.query(Category).filter(Category.title == form.category.data).first()
        product.category = cat.id

        db_sess.add(product)
        db_sess.commit()
        return redirect('/')
    return render_template('product.html', title='Добавление товара', form=form, categories=categories, category=category_flag)


@app.route('/add_to_basket/<int:user_id>/<int:product_id>')
@login_required
def add_to_basket(user_id, product_id):
    db_sess = db_session.create_session()
    products = db_sess.query(Product)
    categories = db_sess.query(Category)
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    if product.count > 0:
        product.count -= 1
        basket = db_sess.query(Basket).filter(Basket.user_id == user_id).first()
        if basket:
            basket.add_product(product_id)
        else:
            new_basket = Basket(user_id=user_id, products_list=str(product_id))
            db_sess.add(new_basket)
        db_sess.commit()
        # redirect('/')
    else:
        return render_template("index.html", title='Lemon Shop', products=products, categories=categories,
                               null=product_id)
    return redirect('/')


@app.route('/basket/<int:id>')
@login_required
def basket(id):
    db_sess = db_session.create_session()
    basket_user = db_sess.query(Basket).filter(Basket.user_id == id).first()
    products_list = []
    if basket_user:
        products_id = basket_user.product_to_list()
        if len(basket_user.products_list) > 0:
            for i in products_id:
                products_list.append(db_sess.query(Product).filter(Product.id == int(i)).first())
    return render_template("basket.html", title='Корзина', products_list=products_list, user_id=id)


@app.route('/buy_product/<int:user_id>/<int:product_id>')
@login_required
def buy_product(user_id, product_id):
    db_sess = db_session.create_session()
    basket_user = db_sess.query(Basket).filter(Basket.user_id == user_id).first()
    basket_user.del_product(str(product_id))
    db_sess.commit()
    return basket(user_id)


@app.route('/cancel_product/<int:user_id>/<int:product_id>')
@login_required
def cancel_product(user_id, product_id):
    db_sess = db_session.create_session()
    basket_user = db_sess.query(Basket).filter(Basket.user_id == user_id).first()
    basket_user.del_product(str(product_id))
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    product.count += 1
    db_sess.commit()
    return basket(user_id)


@app.route('/buy_all/<int:user_id>')
@login_required
def buy_all(user_id):
    db_sess = db_session.create_session()
    basket_user = db_sess.query(Basket).filter(Basket.user_id == user_id).first()
    list_product = basket_user.product_to_list()
    for i in list_product:
        basket_user.del_product(i)
    db_sess.commit()
    return basket(user_id)


@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    form = ProductForm()
    db_sess = db_session.create_session()
    categories = db_sess.query(Category)
    category_flag = ''
    if request.method == "GET":
        product = db_sess.query(Product).filter(Product.id == id).first()

        if product:
            form.title.data = product.title
            picture = product.picture
            form.description.data = product.description
            category_obj = db_sess.query(Category).filter(Category.id == product.category).first()
            category_flag = category_obj.title
            form.category.data = product.category
            form.producer.data = product.producer
            form.price.data = product.price
            form.count.data = product.count
            form.advantage.data = product.advantage
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = db_sess.query(Product).filter(Product.id == id).first()
        category_obj = db_sess.query(Category).filter(Category.id == product.category).first()
        category_flag = category_obj.title

        if product and current_user.is_admin:
            product.title = form.title.data
            if form.picture.data:
                product.picture = form.picture.data
            product.description = form.description.data
            product.category = form.category.data
            product.producer = form.producer.data
            product.price = float(form.price.data)
            product.count = int(form.count.data)
            product.advantage = form.advantage.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    # если у товара есть категория, значит он редактируется
    return render_template('product.html', title='Редоктирование товара', form=form, categories=categories,
                           category=category_flag, picture=picture)


@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id).first()
    if product and current_user.is_admin:
        db_sess.delete(product)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/category')
@login_required
def categories_list():
    if current_user.is_admin:
        db_sess = db_session.create_session()
        category_list = db_sess.query(Category)
        return render_template("category.html", category_list=category_list)
    else:
        abort(404)
        return redirect('/')


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if current_user.is_admin:
        form = AddCategoryForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            category = Category(title=form.title .data, description=form.description.data)
            db_sess.add(category)
            db_sess.commit()
            return redirect('/')
        return render_template('add_category.html', title='Создание категории', form=form)
    else:
        abort(404)
        return redirect('/')


@app.route('/category_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def category_delete(id):
    if current_user.is_admin:
        db_sess = db_session.create_session()
        category = db_sess.query(Category).filter(Category.id == id).first()
        db_sess.delete(category)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/category/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    form = AddCategoryForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        category = db_sess.query(Category).filter(Category.id == id).first()

        if category:
            form.title.data = category.title
            form.description.data = category.description
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        category = db_sess.query(Category).filter(Category.id == id).first()

        if category and current_user.is_admin:
            category.title = form.title.data
            category.description = form.description.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_category.html', title='Редактирование категории', form=form)


if __name__ == '__main__':
    main()
