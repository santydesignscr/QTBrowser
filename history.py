from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QMessageBox, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
import json


class History(QDialog):
    def __init__(self):
        super().__init__()

        self.history = []

        self.load_history()

        self.layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search)

        self.history_list = QListWidget()
        self.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self.show_context_menu)
        self.history_list.itemDoubleClicked.connect(self.open_history_item)

        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.history_list)

        self.setLayout(self.layout)

        self.setWindowTitle('History')
        self.setWindowIcon(QIcon('icons/history.png'))

        self.setMinimumWidth(400)

    def load_history(self):
        try:
            with open('history.json', 'r') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            pass

    def save_history(self):
        with open('history.json', 'w') as f:
            json.dump(self.history, f)

    def add_history_item(self):
        url = self.parent().tabs.currentWidget().url.toString()
        title = self.parent().tabs.currentWidget().web_view.title()
        history_item = {'url': url, 'title': title}
        self.history.append(history_item)
        self.save_history()
        self.show_history()

    def remove_history_item(self):
        index = self.history_list.currentRow()
        if index >= 0:
            self.history.pop(index)
            self.save_history()
            self.show_history()

    def show_history(self):
        self.history_list.clear()
        for history_item in self.history:
            if self.search_bar.text().lower() in history_item['title'].lower() or \
                    self.search_bar.text().lower() in history_item['url'].lower():
                self.history_list.addItem(history_item['title'])

    def open_history_item(self, item):
        index = self.history_list.currentRow()
        if index >= 0:
            url = self.history[index]['url']
            self.parent().tabs.currentWidget().load(QUrl(url))

    def search(self):
        self.show_history()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        remove_action = QAction('Remove', self)
        remove_action.triggered.connect(self.remove_history_item)
        menu.addAction(remove_action)
        menu.exec_(self.history_list.mapToGlobal(pos))