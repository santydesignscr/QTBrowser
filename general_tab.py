from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QWidget


class GeneralTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.dark_mode_checkbox = QCheckBox('Dark Mode')
        self.layout.addWidget(self.dark_mode_checkbox)

        self.setLayout(self.layout)