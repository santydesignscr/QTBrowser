from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QToolBar, QLineEdit, QMenu, QMenuBar, \
    QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from bookmarks import Bookmarks
from downloads import Downloads
from history import History
from password_manager import PasswordManager
from settings import Settings
from tab import Tab


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.tabs)

        self.tabs_list = []

        self.bookmarks = Bookmarks()
        self.downloads = Downloads()
        self.history = History()
        self.password_manager = PasswordManager()
        self.settings = Settings()

        self.create_actions()
        self.create_menus()
        self.create_toolbars()

        self.statusBar().showMessage('Ready')

        self.setWindowTitle('Browser')
        self.setWindowIcon(QIcon('icon.png'))

        self.new_tab()

    def create_actions(self):
        self.new_tab_action = QAction(QIcon('icons/new_tab.png'), 'New Tab', self)
        self.new_tab_action.setShortcut('Ctrl+T')
        self.new_tab_action.triggered.connect(self.new_tab)

        self.new_window_action = QAction(QIcon('icons/new_window.png'), 'New Window', self)
        self.new_window_action.setShortcut('Ctrl+N')
        self.new_window_action.triggered.connect(self.new_window)

        self.close_window_action = QAction(QIcon('icons/close_window.png'), 'Close Window', self)
        self.close_window_action.setShortcut('Ctrl+Shift+W')
        self.close_window_action.triggered.connect(self.close)

        self.close_tab_action = QAction(QIcon('icons/close_tab.png'), 'Close Tab', self)
        self.close_tab_action.setShortcut('Ctrl+W')
        self.close_tab_action.triggered.connect(self.close_tab)

        self.bookmarks_action = QAction(QIcon('icons/bookmarks.png'), 'Bookmarks', self)
        self.bookmarks_action.setShortcut('Ctrl+B')
        self.bookmarks_action.triggered.connect(self.show_bookmarks)

        self.downloads_action = QAction(QIcon('icons/downloads.png'), 'Downloads', self)
        self.downloads_action.setShortcut('Ctrl+J')
        self.downloads_action.triggered.connect(self.show_downloads)

        self.history_action = QAction(QIcon('icons/history.png'), 'History', self)
        self.history_action.setShortcut('Ctrl+H')
        self.history_action.triggered.connect(self.show_history)

        self.password_manager_action = QAction(QIcon('icons/password_manager.png'), 'Password Manager', self)
        self.password_manager_action.setShortcut('Ctrl+Shift+P')
        self.password_manager_action.triggered.connect(self.show_password_manager)

        self.settings_action = QAction(QIcon('icons/settings.png'), 'Settings', self)
        self.settings_action.setShortcut('Ctrl+Shift+S')
        self.settings_action.triggered.connect(self.show_settings)

        self.exit_action = QAction(QIcon('icons/exit.png'), 'Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(self.close)

    def create_menus(self):
        self.file_menu = QMenu('File', self)
        self.file_menu.addAction(self.new_tab_action)
        self.file_menu.addAction(self.new_window_action)
        self.file_menu.addAction(self.close_window_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.edit_menu = QMenu('Edit', self)
        self.edit_menu.addAction(self.bookmarks_action)
        self.edit_menu.addAction(self.downloads_action)
        self.edit_menu.addAction(self.history_action)
        self.edit_menu.addAction(self.password_manager_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.settings_action)

        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.edit_menu)

    def create_toolbars(self):
        self.toolbar = QToolBar('Toolbar', self)
        self.toolbar.addAction(self.new_tab_action)
        self.toolbar.addAction(self.close_tab_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.bookmarks_action)
        self.toolbar.addAction(self.downloads_action)
        self.toolbar.addAction(self.history_action)
        self.toolbar.addAction(self.password_manager_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.settings_action)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search)
        self.toolbar.addWidget(self.search_bar)

    def new_tab(self):
        tab = Tab(self)
        self.tabs.addTab(tab, 'New Tab')
        self.tabs.setCurrentWidget(tab)
        self.tabs_list.append(tab)

    def new_window(self):
        browser = Browser()
        browser.show()

    def close_tab(self, index=None):
        if index is None:
            index = self.tabs.currentIndex()
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
            self.tabs_list.pop(index)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def show_bookmarks(self):
        self.bookmarks.show()

    def show_downloads(self):
        self.downloads.show()

    def show_history(self):
        self.history.show()

    def show_password_manager(self):
        self.password_manager.show()

    def show_settings(self):
        self.settings.show()

    def search(self):
        url = self.search_bar.text()
        if 'http' not in url:
            url = 'https://' + url
        self.tabs.currentWidget().load(QUrl(url))

    def tab_changed(self, index):
        if len(self.tabs_list) > 0 and index < len(self.tabs_list):
            current_tab = self.tabs_list[index]
            current_tab.url_bar.setText(current_tab.web_view.url().toString())
    
    def update_url(self, url):
        if len(self.tabs_list) > 0:
            self.tabs_list[self.tabs.currentIndex()].url_bar.setText(url.toString())