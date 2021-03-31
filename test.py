# Добавление админа
import main
from data import db_session
from data.users import User


db_session.global_init("db/shop.db")
db_sess = db_session.create_session()
user = User()

user = User(
            surname='Admin',
            name='Shop',
            email='admin_shop@lemon.org',
            phone='+78888888888',
            address='Главный офис',
            is_admin=True
        )
user.set_password('123')
db_sess.add(user)
db_sess.commit()
