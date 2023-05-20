from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QMessageBox, QMenu, QAction, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem, QWebEngineProfile
import os


class Downloads(QDialog):
    def __init__(self):
        super().__init__()

        self.downloads = []

        self.layout = QVBoxLayout()

        self.downloads_list = QListWidget()
        self.downloads_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.downloads_list.customContextMenuRequested.connect(self.show_context_menu)

        self.layout.addWidget(self.downloads_list)

        self.setLayout(self.layout)

        self.setWindowTitle('Downloads')
        self.setWindowIcon(QIcon('icons/downloads.png'))

        self.setMinimumWidth(400)

    def download_requested(self, download):
        download.finished.connect(self.download_finished)
        self.downloads.append(download)
        self.show_downloads()

    def download_finished(self):
        self.show_downloads()

    def show_downloads(self):
        self.downloads_list.clear()
        for download in self.downloads:
            item = QListWidgetItem(download.url().fileName())
            progress_bar = QProgressBar()
            progress_bar.setMaximum(download.totalBytes())
            progress_bar.setValue(download.receivedBytes())
            progress_bar.setFormat('{:.2f} MB / {:.2f} MB'.format(download.receivedBytes() / 1024 / 1024,
                                                                   download.totalBytes() / 1024 / 1024))
            item.setSizeHint(progress_bar.sizeHint())
            self.downloads_list.addItem(item)
            self.downloads_list.setItemWidget(item, progress_bar)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        remove_action = QAction('Remove', self)
        remove_action.triggered.connect(self.remove_download)
        menu.addAction(remove_action)
        menu.exec_(self.downloads_list.mapToGlobal(pos))

    def remove_download(self):
        index = self.downloads_list.currentRow()
        if index >= 0:
            self.downloads.pop(index)
            self.show_downloads()