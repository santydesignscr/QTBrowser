from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QMessageBox, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
import json


class Bookmarks(QDialog):
    def __init__(self):
        super().__init__()

        self.bookmarks = []

        self.load_bookmarks()

        self.layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search)

        self.bookmarks_list = QListWidget()
        self.bookmarks_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bookmarks_list.customContextMenuRequested.connect(self.show_context_menu)
        self.bookmarks_list.itemDoubleClicked.connect(self.open_bookmark)

        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.bookmarks_list)

        self.setLayout(self.layout)

        self.setWindowTitle('Bookmarks')
        self.setWindowIcon(QIcon('icons/bookmarks.png'))

        self.setMinimumWidth(400)

    def load_bookmarks(self):
        try:
            with open('bookmarks.json', 'r') as f:
                self.bookmarks = json.load(f)
        except FileNotFoundError:
            pass

    def save_bookmarks(self):
        with open('bookmarks.json', 'w') as f:
            json.dump(self.bookmarks, f)

    def add_bookmark(self):
        url = self.parent().tabs.currentWidget().url.toString()
        title = self.parent().tabs.currentWidget().web_view.title()
        bookmark = {'url': url, 'title': title}
        self.bookmarks.append(bookmark)
        self.save_bookmarks()
        self.show_bookmarks()

    def remove_bookmark(self):
        index = self.bookmarks_list.currentRow()
        if index >= 0:
            self.bookmarks.pop(index)
            self.save_bookmarks()
            self.show_bookmarks()

    def show_bookmarks(self):
        self.bookmarks_list.clear()
        for bookmark in self.bookmarks:
            if self.search_bar.text().lower() in bookmark['title'].lower() or \
                    self.search_bar.text().lower() in bookmark['url'].lower():
                self.bookmarks_list.addItem(bookmark['title'])

    def open_bookmark(self, item):
        index = self.bookmarks_list.currentRow()
        if index >= 0:
            url = self.bookmarks[index]['url']
            self.parent().tabs.currentWidget().load(QUrl(url))

    def search(self):
        self.show_bookmarks()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        remove_action = QAction('Remove', self)
        remove_action.triggered.connect(self.remove_bookmark)
        menu.addAction(remove_action)
        menu.exec_(self.bookmarks_list.mapToGlobal(pos))