import unittest
from DataBase import db_session
from app import app
import json

name_test_bd = 'DataBase/data_base.db'
login_user = 'test_login'
password_user = 'test_password'


class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = True
        db_session.global_init(name_test_bd)
        self.app = app.test_client()
        register = self.app.get('/register_user', json={'login': 'test_login', 'password': 'test_password'})
        self.json_register = register.get_json()
        assert self.json_register['condition'] == 'success'
        assert 'key_user' in self.json_register['parameters']

    def tearDown(self) -> None:
        login = self.app.get('/login_user', json={'login': 'test_login', 'password': 'test_password'})
        json_login = login.get_json()
        assert json_login['condition'] == 'success'
        key_user = json_login['parameters']['key_user']
        remove_user = self.app.get('/delete_user', json={'key_user': key_user})
        json_remove_user = remove_user.get_json()
        assert json_remove_user['condition'] == 'success'

    # Тестирования входа в систему
    def test_login(self):
        login = self.app.get('/login_user', json={'login': 'test_login', 'password': 'test_password'})
        condition_login = login.get_json()['condition']
        assert condition_login == 'success'

    # Тестирование основной работы программы. Добавление продукта, редактирование продукта,
    # просмотр всех продуктов, удаление продукта
    def test_add_product_and_get_products_and_remove(self):
        key_user = self.json_register['parameters']['key_user']
        add_product = self.app.get('/add_product', json={'key_user': key_user,
                                                         'date_purchase': '2021-03-16T00:00:00',
                                                         'name_product': 'cake',
                                                         'price_product': 300.0})
        json_add_product = add_product.get_json()
        assert json_add_product['condition'] == 'success'
        get_list_products = self.app.get('/get_list_products', json={'key_user': key_user})
        json_get_products = json.loads(get_list_products.get_data())
        assert json_get_products['condition'] == 'success'
        change_product = self.app.get('/edit_product', json={'key_user': key_user,
                                                             'id_product': json_add_product['parameters'][
                                                                 'id_product'],
                                                             'date_purchase': '2021-03-16T00:00:00',
                                                             'name_product': 'apple',
                                                             'price_product': 250.5})
        json_change_product = change_product.get_json()
        assert json_change_product['condition'] == 'success'

        remove_product = self.app.get('/delete_product', json={'key_user': key_user,
                                                               'id_product': json_add_product['parameters'][
                                                                   'id_product']})
        json_remove_product = remove_product.get_json()
        assert json_remove_product['condition'] == 'success'


if __name__ == '__main__':
    unittest.main()
