import flask
from flask import jsonify, request
from DataBase.user import User
from DataBase.product import Product
from DataBase import db_session
from generate_key_user import generator_key

character_valid = "qwertyuiopasdfghjklzxcvbnm1234567890-."
blueprint = flask.Blueprint('api', __name__, template_folder="templates")


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