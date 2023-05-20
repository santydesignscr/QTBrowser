from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget
from general_tab import GeneralTab
from security_tab import SecurityTab


class Settings(QDialog):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()

        self.general_tab = GeneralTab()
        self.security_tab = SecurityTab()

        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.security_tab, "Security")

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)