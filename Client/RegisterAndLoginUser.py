from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QDesktopWidget, QMainWindow, QLabel, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox


# Вход пользователя в аккаунт
class LoginUser(QMainWindow):
    def __init__(self, parent=None):
        super(LoginUser, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.closable = False
        self.button_register.clicked.connect(self.parent.select_register)
        self.button_enter.clicked.connect(self.sent_parameters)

    def __init_ui(self):
        widget = QWidget()
        vbox = QVBoxLayout()
        # Название окна
        self.title_program = QLabel('Вход')
        self.title_program.setAlignment(Qt.AlignCenter)

        # Поле логина
        self.label_login = QLabel('Логин')
        self.line_edit_login = QLineEdit()
        self.line_edit_login.setPlaceholderText('Введите логин')
        hbox_login = QHBoxLayout()
        hbox_login.addWidget(self.label_login)
        hbox_login.addWidget(self.line_edit_login)

        # Поле пароля
        self.label_password = QLabel('Пароль')
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        self.line_edit_password.setPlaceholderText('Введите пароль')
        hbox_password = QHBoxLayout()
        hbox_password.addWidget(self.label_password)
        hbox_password.addWidget(self.line_edit_password)

        # Кнопка для входа
        self.button_enter = QPushButton('Вход')
        # Кнопка, чтобы перейти на регистрацию
        self.button_register = QPushButton('Регистрация')

        # Расположение элементов на экране
        vbox.addWidget(self.title_program)
        vbox.addLayout(hbox_login)
        vbox.addLayout(hbox_password)
        vbox.addWidget(self.button_enter)
        vbox.addWidget(self.button_register)
        widget.setLayout(vbox)

        self.setCentralWidget(widget)

        self.resize(350, 150)
        self.center()

        self.setWindowTitle('NoteBook Login')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Отправка параметров после ввода всех данных
    def sent_parameters(self):
        self.parent.passing_parameters_login_register(condition_login=True,
                                                      login=self.line_edit_login.text(),
                                                      password=self.line_edit_password.text(), widget=self)

    def closeEvent(self, event) -> None:
        if self.closable:
            super(LoginUser, self).closeEvent(event)
        else:
            event.ignore()


# Регистрация пользователя в системе
class RegisterUser(QMainWindow):
    def __init__(self, parent=None):
        super(RegisterUser, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.closable = False
        # Нажатие на кнопки
        self.button_login.clicked.connect(parent.select_login)
        self.button_enter.clicked.connect(self.sent_parameters)

    def __init_ui(self):
        widget = QWidget()
        vbox = QVBoxLayout()
        # Название окна
        self.title_program = QLabel('Регистрация')
        self.title_program.setAlignment(Qt.AlignCenter)

        # Поле логина
        self.label_login = QLabel('Логин')
        self.line_edit_login = QLineEdit()
        self.line_edit_login.setPlaceholderText('Введите логин')
        hbox_login = QHBoxLayout()
        hbox_login.addWidget(self.label_login)
        hbox_login.addWidget(self.line_edit_login)

        # Поле пароля
        self.label_password = QLabel('Пароль')
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setPlaceholderText('Введите пароль')
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        hbox_password = QHBoxLayout()
        hbox_password.addWidget(self.label_password)
        hbox_password.addWidget(self.line_edit_password)

        # Поле повторного пароля
        self.label_replay_password = QLabel('Повторите пароль')
        self.line_edit_replay_password = QLineEdit()
        self.line_edit_replay_password.setPlaceholderText('Введите пароль повторно')
        self.line_edit_replay_password.setEchoMode(QLineEdit.Password)
        hbox_replay_password = QHBoxLayout()
        hbox_replay_password.addWidget(self.label_replay_password)
        hbox_replay_password.addWidget(self.line_edit_replay_password)

        # Кнопка для входа
        self.button_enter = QPushButton('Регистрация')
        # Кнопка чтобы перейти на логин
        self.label_have_login = QLabel('Уже есть аккаунт?')
        self.button_login = QPushButton('Логин')
        hbox_have_login = QHBoxLayout()
        hbox_have_login.addWidget(self.label_have_login)
        hbox_have_login.addWidget(self.button_login)

        # Расположение элементов на экране
        vbox.addWidget(self.title_program)
        vbox.addLayout(hbox_login)
        vbox.addLayout(hbox_password)
        vbox.addLayout(hbox_replay_password)
        vbox.addWidget(self.button_enter)
        vbox.addLayout(hbox_have_login)
        widget.setLayout(vbox)

        self.setCentralWidget(widget)

        self.resize(350, 150)
        self.center()

        self.setWindowTitle('NoteBook Register')

    # Отправка параметров после ввода всех данных
    def sent_parameters(self):
        if self.__check_password():
            self.parent.passing_parameters_login_register(condition_login=False,
                                                          login=self.line_edit_login.text(),
                                                          password=self.line_edit_password.text(),
                                                          replace_password=self.label_replay_password.text(),
                                                          widget=self)

    # Проверка пароля.
    # Пароль должен состоять из 8 и более символов.
    # Пароль должен содержать хотя бы одну цифру и заглавную букву
    # Пароли должны совпадать
    def __check_password(self):
        dict_errors = {
            'short': False,
            'no_number': True,
            'no_upper_later': True,
            'do_not_match': False
        }
        password_one = self.line_edit_password.text()
        password_two = self.line_edit_replay_password.text()
        # Проверка, что пароль длиннее 8 символов
        if len(password_one) < 8:
            dict_errors['short'] = True
        for sign in password_one:
            if sign in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                dict_errors['no_number'] = False
            elif sign == sign.upper():
                dict_errors['no_upper_later'] = False
        if password_one != password_two:
            dict_errors['do_not_match'] = True

        text_error = f'''Ошибка при вводе пароля. Проверьте следующие параметры:\n
        1.Пароль длинее 8 символов\n
        2.Пароль имеетя хотя бы одну цифру\n
        3.Пароль имеет хотя бы одну заглавную букву\n
        4.Пароли совпадают'''

        for key in dict_errors.keys():
            if dict_errors[key] is True:
                QMessageBox.critical(self, 'Ошибка', text_error, QMessageBox.Ok)
                return False
        return True

    def closeEvent(self, event) -> None:
        if self.closable:
            super(RegisterUser, self).closeEvent(event)
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
