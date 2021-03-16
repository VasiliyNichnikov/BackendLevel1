import flask
from flask import jsonify, request
from DataBase.user import User
from DataBase.product import Product
from DataBase import db_session
from generate_key_user import generator_key
from json import JSONEncoder
import dateutil.parser
import json
import datetime

character_valid = "qwertyuiopasdfghjklzxcvbnm1234567890-."
blueprint = flask.Blueprint('api', __name__, template_folder="templates")


def decode_datetime(emp_dict):
    if 'date_purchase' in emp_dict:
        emp_dict["date_purchase"] = dateutil.parser.parse(emp_dict["date_purchase"])
    return emp_dict


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


@blueprint.route('/register_user', methods=['GET', 'POST'])
def register_user():
    """
    Регистрация пользователя в БД
    Зарегистрироваться можно двумя способами
    Используя логин и пароль
    """
    if not request.json:
        return jsonify({'condition': 'error', 'parameters': {'key_error': '101', 'description': 'nothing passed'}})
    answer = request.json
    session = db_session.create_session()
    if 'login' not in answer or 'password' not in answer:
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': '201', 'description': 'no required parameters for registration'}})

    login, password = answer['login'], answer['password']

    if session.query(User).filter(User.login == login).first():
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': '301',
                                       'description': 'login is busy'}})
    user = User(
        login=login
    )
    user.set_password(password)
    # В бесконечном цикле проверяем, чтобы ключ сгенерировался уникальным
    while True:
        generate_key = generator_key(50)
        if session.query(User).filter(User.key_user == generate_key).first() is None:
            break
    user.key_user = generate_key
    session.add(user)
    session.commit()

    return jsonify({'condition': 'success', 'parameters': {'key_user': generate_key}})


@blueprint.route('/login_user', methods=['GET', 'POST'])
def login_user():
    """
        Вход в аккаунт
        Для входа в аккаунт нужно передать
        логин и пароль
        Функция вернет ключ пользователя, если данный пользователь есть в списках
    """
    if not request.json:
        return jsonify({'condition': 'error', 'parameters': {'key_error': '101', 'description': 'nothing passed'}})

    answer = request.json
    session = db_session.create_session()
    if 'login' not in answer or 'password' not in answer:
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': '202', 'description': 'no need of login credentials'}})

    login, password = answer['login'], answer['password']
    user = session.query(User).filter(User.login == login).first()
    if user is None or not user.check_password(password):
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': '401',
                                       'description': 'user not found'}})
    return jsonify({'condition': 'success', 'parameters': {'key_user': user.key_user}})


@blueprint.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """
        Добавление продукта в список пользователя
        Для добавления товара нужно передать слудующие параметры:
        1) ключ пользователя
        2) дата покупки товара
        3) название товара
        4) цена товара
    """
    if not request.json:
        return jsonify({'condition': 'error', 'parameters': {'key_error': '101', 'description': 'nothing passed'}})
    answer = json.loads(request.data, object_hook=decode_datetime)
    session = db_session.create_session()
    if 'key_user' not in answer \
            or 'date_purchase' not in answer \
            or 'name_product' not in answer \
            or 'price_product' not in answer:
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': '203',
                                       'description': 'there are no necessary parameters for adding the product'}})

    key_user, date_purchase, name_product, price_product = answer['key_user'], \
                                                           answer['date_purchase'], \
                                                           answer['name_product'], \
                                                           answer['price_product']
    user = session.query(User).filter(User.key_user == key_user).first()
    if user is None:
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': '401',
                                       'description': 'user not found'}})
    if type(price_product) != float:
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': 'TypeError',
                                       'description': 'Type price_product != float'}})

    try:
        product = Product(date_purchase=datetime.datetime(date_purchase.year, date_purchase.month, date_purchase.day),
                          name_product=name_product,
                          price_product=price_product)
    except TypeError as e:
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': 'TypeError',
                                       'description': 'type error - %s' % e}})
    except ValueError as e:
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': 'ValueError',
                                       'description': 'value error - %s' % e}})
    user.products.append(product)
    session.commit()
    return jsonify({'condition': 'success', 'parameters': {'id_product': product.id}})


@blueprint.route('/get_list_products', methods=['GET', 'POST'])
def get_list_products():
    """
        Получение списка товаров пользователя
        Для получения списка нужно отправить ключ пользовател
        При успешной работе, функция вернет список товаров
    """
    if not request.json:
        return jsonify({'condition': 'error', 'parameters': {'key_error': '101', 'description': 'nothing passed'}})

    answer = request.json
    session = db_session.create_session()
    if 'key_user' not in answer:
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': '204',
                                       'description': 'key_user not passed'}})

    key_user = answer['key_user']
    user = session.query(User).filter(User.key_user == key_user).first()
    if user is None:
        return jsonify({'condition': 'error',
                        'parameters': {'key_error': '401',
                                       'description': 'user not found'}})
    products = user.products
    list_products = []
    for product in products:
        dict_product = {
            'id_product': product.id,
            'date_purchase': product.date_purchase,
            'name_product': product.name_product,
            'price_product': product.price_product
        }
        list_products.append(dict_product)
    return json.dumps({'condition': 'success', 'parameters': {'list_products': list_products}},
                      indent=4, cls=DateTimeEncoder)