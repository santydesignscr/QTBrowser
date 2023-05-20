from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QWidget


class SecurityTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.passwords_checkbox = QCheckBox('Manage Passwords')
        self.layout.addWidget(self.passwords_checkbox)

        self.setLayout(self.layout)