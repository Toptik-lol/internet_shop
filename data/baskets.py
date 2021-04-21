import sqlalchemy

from .db_session import SqlAlchemyBase


class Basket(SqlAlchemyBase):
    __tablename__ = 'baskets'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    # в поле хранится id товаров, разделитель ', '
    products_list = sqlalchemy.Column(sqlalchemy.String(convert_unicode=True))

    def add_product(self, product_id):
        if len(str(self.products_list)) > 0:
            self.products_list = str(self.products_list) + ', ' + str(product_id)
        else:
            self.products_list = str(product_id)

    def product_to_list(self):
        return self.products_list.split(', ')

    def del_product(self, product_id):
        list_prod = self.product_to_list()
        index = list_prod.index(product_id)
        del list_prod[index]
        li = ", ".join(list_prod)
        self.products_list = li
