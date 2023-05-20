from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QMessageBox, QMenu, QAction, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
import json
import hashlib


class PasswordManager(QDialog):
    def __init__(self):
        super().__init__()

        self.passwords = []

        self.load_passwords()

        self.layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search)

        self.passwords_list = QListWidget()
        self.passwords_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.passwords_list.customContextMenuRequested.connect(self.show_context_menu)
        self.passwords_list.itemDoubleClicked.connect(self.show_password)

        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.passwords_list)

        self.setLayout(self.layout)

        self.setWindowTitle('Password Manager')
        self.setWindowIcon(QIcon('icons/password_manager.png'))

        self.setMinimumWidth(400)

    def load_passwords(self):
        try:
            with open('passwords.json', 'r') as f:
                self.passwords = json.load(f)
        except FileNotFoundError:
            pass

    def save_passwords(self):
        with open('passwords.json', 'w') as f:
            json.dump(self.passwords, f)

    def add_password(self):
        url = self.parent().tabs.currentWidget().url.toString()
        username, ok = QInputDialog.getText(self, 'Username', 'Enter username:')
        if ok:
            password, ok = QInputDialog.getText(self, 'Password', 'Enter password:', QLineEdit.Password)
            if ok:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                password_item = {'url': url, 'username': username, 'password': password_hash}
                self.passwords.append(password_item)
                self.save_passwords()
                self.show_passwords()

    def remove_password(self):
        index = self.passwords_list.currentRow()
        if index >= 0:
            self.passwords.pop(index)
            self.save_passwords()
            self.show_passwords()

    def show_passwords(self):
        self.passwords_list.clear()
        for password_item in self.passwords:
            if self.search_bar.text().lower() in password_item['url'].lower() or \
                    self.search_bar.text().lower() in password_item['username'].lower():
                self.passwords_list.addItem(password_item['url'] + ' - ' + password_item['username'])

    def show_password(self, item):
        index = self.passwords_list.currentRow()
        if index >= 0:
            password_item = self.passwords[index]
            password, ok = QInputDialog.getText(self, 'Password', 'Enter password:', QLineEdit.Password)
            if ok:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                if password_hash == password_item['password']:
                    QMessageBox.information(self, 'Password', 'Username: {}\nPassword: {}'.format(
                        password_item['username'], password_item['password']))
                else:
                    QMessageBox.warning(self, 'Password', 'Incorrect password')

    def search(self):
        self.show_passwords()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        remove_action = QAction('Remove', self)
        remove_action.triggered.connect(self.remove_password)
        menu.addAction(remove_action)
        menu.exec_(self.passwords_list.mapToGlobal(pos))