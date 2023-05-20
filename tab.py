from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile


class Tab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.layout = QVBoxLayout()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)

        self.web_view = QWebEngineView()
        self.web_view.urlChanged.connect(self.update_url)

        self.layout.addWidget(self.url_bar)
        self.layout.addWidget(self.web_view)

        self.setLayout(self.layout)

        self.load(QUrl('https://www.google.com'))

    def load(self, url):
        self.web_view.load(url)

    def load_url(self):
        url = self.url_bar.text()
        if 'http' not in url:
            url = 'https://' + url
        self.load(QUrl(url))

    def update_url(self, url):
        self.parent.update_url(url)