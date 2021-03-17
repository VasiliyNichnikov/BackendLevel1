import sys
import os
import json
import datetime
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QDoubleValidator
from ConnectingServer import ConnectingServer
import dateutil.parser
from RegisterAndLoginUser import RegisterUser, LoginUser
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QDesktopWidget, QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtWidgets import QListWidget, QPushButton, QListWidgetItem, QFrame, QLineEdit, QDateEdit
from PyQt5.QtWidgets import QMessageBox


def decode_datetime(emp_dict):
    if 'date_purchase' in emp_dict:
        emp_dict["date_purchase"] = dateutil.parser.parse(emp_dict["date_purchase"])
    return emp_dict


# Класс виджета, который отображает продукт
class WidgetNote(QWidget):

    def __init__(self, parent=None):
        super(WidgetNote, self).__init__(parent)
        self.parent = parent
        # Состояние компонентов (Можно редактировать или нет)
        self.condition_edit = True
        # Создание интерфейса
        self.__init_ui()
        # id товара
        self.product_id = 0
        # Включение Read Only
        self.read_only_on_off()
        # Подключение кнопок
        self.button_edit.clicked.connect(self.__button_edit_input)
        self.button_remove.clicked.connect(self.parent.remove_product_list)

    def __init_ui(self):
        hbox = QHBoxLayout()
        self.name_product = QLineEdit()
        self.name_product.setPlaceholderText('Введите название товара')
        self.price_product = QLineEdit()
        self.price_product.setValidator(QDoubleValidator())
        self.price_product.setPlaceholderText('Введите цену товара')
        current_date = QDate()
        self.date_purchase = QDateEdit()
        self.date_purchase.setDate(current_date.currentDate())
        self.button_edit = QPushButton('Редактировать')
        self.button_remove = QPushButton('Удалить')
        hbox.addWidget(self.name_product)
        hbox.addWidget(QVLine())
        hbox.addWidget(self.price_product)
        hbox.addWidget(QVLine())
        hbox.addWidget(self.date_purchase)
        hbox.addWidget(QVLine())
        hbox.addWidget(self.button_edit)
        hbox.addWidget(QVLine())
        hbox.addWidget(self.button_remove)
        self.setLayout(hbox)

    # Включение/выключение 'read only'
    def read_only_on_off(self) -> None:
        self.condition_edit = not self.condition_edit
        if self.condition_edit:
            self.button_edit.setText('Редактировать')
        else:
            self.button_edit.setText('Сохранить')

        self.name_product.setReadOnly(self.condition_edit)
        self.price_product.setReadOnly(self.condition_edit)
        self.date_purchase.setReadOnly(self.condition_edit)

    def __button_edit_input(self):
        self.read_only_on_off()

        if self.name_product.text() == '':
            self.name_product.setText('Product Name')

        if self.condition_edit:
            self.parent.edit_product(product_id=self.product_id, name_product=self.name_product.text(),
                                     price_product=self.convert_price(), date_purchase=self.convert_date())

    def select_name_product(self, text) -> None:
        self.name_product.setText(text)

    def select_price_product(self, text) -> None:
        self.price_product.setText(text)

    def select_id_product(self, id):
        self.product_id = id

    def select_date_purchase(self, date):
        qt_date = QDate()
        qt_date.setDate(date.year, date.month, date.day)
        self.date_purchase.setDate(qt_date)

    # Преобразовать дату
    def convert_date(self):
        day, month, year = self.date_purchase.text().split('.')
        return datetime.datetime(int(year), int(month), int(day))

    # Преобразовать цену
    def convert_price(self):
        price = self.price_product.text()
        if price != '':
            if ',' in price:
                return float(price.replace(',', '.'))
            return float(price)
        self.price_product.setText('0.0')
        return 0.0


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__init_ui()
        # Создание класса, отвечающего за подключение к серверу
        self.connecting_server = ConnectingServer('http://localhost:8000')
        # Путь до файла с json
        self.path_json = 'user_data.json'
        # Окна логина и регистрации
        self.window_login = None
        self.window_register = None

        # Проверка, что ключ пользователь существует
        self.load_key_and_login()
        if self.key_user == '':
            self.setEnabled(False)
            self.select_login()
        else:
            self.get_products_from_server()

        # Нажатие на кнопки
        self.button_add_note.clicked.connect(self.__add_element_list)
        self.button_exit_user.clicked.connect(self.__exit_user)
        self.button_remove_user.clicked.connect(self.__remove_user)

    def __init_ui(self):
        widget = QWidget()
        vbox = QVBoxLayout()
        # Название программы
        self.title_program = QLabel('Записная книжка')
        self.title_program.setAlignment(Qt.AlignCenter)
        # Логин пользователя
        self.login_user = QLabel('Логин')
        self.button_remove_user = QPushButton('Удалить аккаунт')
        self.button_exit_user = QPushButton('Выход из аккаунта')
        hbox_user = QHBoxLayout()
        hbox_user.addWidget(self.login_user)
        hbox_user.addWidget(self.button_remove_user)
        hbox_user.addWidget(self.button_exit_user)
        # Кнопка добавления новых заметок
        self.button_add_note = QPushButton('Добавить продукт')
        # Список заметок
        self.list_notes = QListWidget()
        # Список QListItem
        self.list_widgets_products = []
        # Расположение элементов на экране
        vbox.addWidget(self.title_program)
        vbox.addLayout(hbox_user)
        vbox.addWidget(self.list_notes)
        vbox.addWidget(self.button_add_note)
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.resize(350, 400)
        self.center()

        self.setWindowTitle('NoteBook')
        self.show()

    # Добавление элемента в список
    def __add_element_list(self):
        now = datetime.datetime.now()
        condition, parameters = self.add_product_server(name_product='Product Name',
                                                        date_purchase=datetime.datetime(now.year, now.month, now.day),
                                                        price_product=0.0)
        if condition:
            self.__add_product(parameters['id_product'])
            self.__add_horizontal_line()

    # Редактирование продукта
    def edit_product(self, product_id, name_product, price_product, date_purchase):
        result = self.connecting_server.edit_product(key_user=self.key_user,
                                                     product_id=product_id,
                                                     name_product=name_product,
                                                     date_purchase=date_purchase,
                                                     price_product=price_product)
        if result['condition'] != 'error':
            if result['result'].ok:
                result_json = result['result'].json()
                if result_json['condition'] != 'success':
                    QMessageBox.critical(self, 'Ошибка', f'Ошибка при передачи параметров на сервер - '
                                                         f'{result_json["parameters"]["key_error"]}', QMessageBox.Ok)

            else:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)

    # Удаление продукта из списка
    def remove_product_list(self):
        for item in self.list_widgets_products:
            widget = self.list_notes.itemWidget(item)
            if widget.button_remove == self.sender():
                index_remove_item = self.list_notes.row(item)
                if self.remove_product_server(widget.product_id):
                    self.list_widgets_products.remove(item)
                    self.list_notes.takeItem(index_remove_item + 1)
                    self.list_notes.takeItem(index_remove_item)
                break

    # Удаление продукта на сервере
    def remove_product_server(self, product_id):
        result = self.connecting_server.remove_product(key_user=self.key_user,
                                                       id_product=product_id)
        if result['condition'] != 'error':
            if result['result'].ok:
                result_json = result['result'].json()
                return result_json['condition'] == 'success'
            else:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)
                return False
        else:
            QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)
            return False

    # Добавление элемента продукта в список
    def __add_product(self, product_id) -> WidgetNote:
        product = WidgetNote(self)
        product.select_id_product(product_id)
        list_widget_item = QListWidgetItem(self.list_notes)
        list_widget_item.setSizeHint(product.sizeHint())
        self.list_widgets_products.append(list_widget_item)
        self.list_notes.addItem(list_widget_item)
        self.list_notes.setItemWidget(list_widget_item, product)
        return product

    def load_key_and_login(self):
        self.key_user, self.login = self.__get_user_key_and_login()
        self.login_user.setText(self.login)

    # Добавление элемента горизонтальной линии
    def __add_horizontal_line(self) -> None:
        line = QHLine()
        list_widget_item = QListWidgetItem(self.list_notes)
        list_widget_item.setSizeHint(line.sizeHint())
        self.list_notes.addItem(list_widget_item)
        self.list_notes.setItemWidget(list_widget_item, line)

    # Получение ключа и логина из файла
    def __get_user_key_and_login(self):
        if os.path.exists(self.path_json):
            with open(self.path_json, 'r', encoding='utf-8') as read_file:
                data = json.load(read_file)
                return data['key_user'], data['login']
        else:
            QMessageBox.critical(self, 'Ошибка', 'Json файл не найден', QMessageBox.Ok)
        return False

    # Добавление продукта на сервер
    def add_product_server(self, name_product, date_purchase, price_product):
        result = self.connecting_server.add_product(key_user=self.key_user,
                                                    name_product=name_product,
                                                    date_purchase=date_purchase,
                                                    price_product=price_product)
        if result['condition'] != 'error':
            if result['result'].ok:
                condition = result['result'].json()['condition']
                parameters = result['result'].json()['parameters']
                return condition == 'success', parameters
            else:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)
                return False, None
        else:
            QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)
            return False, None

    # Сохранение информации о пользователе
    def __save_user_info(self, data):
        if os.path.exists(self.path_json):
            with open(self.path_json, 'w', encoding='utf-8') as write_file:
                json.dump(data, write_file)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Json файл не найден', QMessageBox.Ok)

    # Выбор окна "Логин"
    def select_login(self):
        if self.window_register is not None:
            self.window_register.closable = True
            self.window_register.close()
            self.window_register = None

        self.window_login = LoginUser(self)
        self.window_login.show()

    # Выбор окна "Регистрация"
    def select_register(self):
        if self.window_login is not None:
            self.window_login.closable = True
            self.window_login.close()
            self.window_login = None

        self.window_register = RegisterUser(self)
        self.window_register.show()

    # Вход в систему
    def __login_user(self, login, password, widget, register_user=False):
        if not register_user:
            result = self.connecting_server.connect_user(login, password)
        else:
            result = self.connecting_server.register_user(login, password)
        if result['condition'] != 'error':
            if result['result'].ok:
                result_json = result['result'].json()
                if result_json['condition'] == 'success':
                    key_user = result_json['parameters']['key_user']
                    self.__save_user_info({'login': login, 'key_user': key_user})
                    widget.closable = True
                    widget.close()
                    self.setEnabled(True)
                    # Загрузка данных из файла
                    self.load_key_and_login()
                    if not register_user:
                        self.get_products_from_server()
                else:
                    QMessageBox.critical(self, 'Ошибка', f'Ошибка при передачи параметров на сервер - '
                                                         f'{result_json["parameters"]["key_error"]}', QMessageBox.Ok)
            else:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)

    # Выход из системы
    def __exit_user(self):
        # Очистка списка с продуктами
        self.list_notes.clear()
        # Перезаписать json файл
        self.__save_user_info({'login': 'Login', 'key_user': ''})
        # Меняем надпись логина
        self.login_user.setText('Login')
        # Запускаем окно для входа или регистрации
        self.setEnabled(False)
        self.select_login()

    # Удалить аккаунт из БД
    def __remove_user(self):
        result = self.connecting_server.remove_user(key_user=self.key_user)
        if result['condition'] != 'error':
            if result['result'].ok:
                condition = result['result'].json()['condition']
                if condition == 'success':
                    self.__exit_user()
            else:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)

    # Получение продуктов, которые есть на сервере у пользователя
    def get_products_from_server(self):
        result = self.connecting_server.get_products(key_user=self.key_user)
        if result['condition'] != 'error':
            if result['result'].ok:
                result_json = json.loads(result['result'].text, object_hook=decode_datetime)
                if result_json['condition'] == 'success':
                    parameters = result_json['parameters']
                    for product in parameters['list_products']:
                        element_product = self.__add_product(product['id_product'])
                        element_product.condition_edit = False
                        element_product.read_only_on_off()
                        element_product.select_name_product(product['name_product'])
                        element_product.select_price_product(str(product['price_product']))
                        element_product.select_date_purchase(product['date_purchase'])
                        self.__add_horizontal_line()
                else:
                    parameters = result['result'].json()['parameters']
                    # Данная ошибка сообщает о том, что пользователь не найден
                    if parameters['key_error'] == '401':
                        self.__exit_user()
                    QMessageBox.critical(self, 'Ошибка', f'Ошибка при передачи параметров на сервер - '
                                                         f'{parameters["key_error"]}', QMessageBox.Ok)
            else:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Ошибка', 'Ошибка при подключении к серверу', QMessageBox.Ok)

    # Передача параметров после регистрации или входа в аккаунт
    def passing_parameters_login_register(self, **kwargs):
        if kwargs['condition_login']:
            self.__login_user(login=kwargs['login'], password=kwargs['password'], widget=kwargs['widget'],
                              register_user=False)
        else:
            self.__login_user(login=kwargs['login'], password=kwargs['password'], widget=kwargs['widget'],
                              register_user=True)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event) -> None:
        if self.window_login is not None:
            self.window_login.closable = True
            self.window_login.close()
        if self.window_register is not None:
            self.window_register.closable = True
            self.window_register.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    sys.exit(app.exec_())
