import sys
from PyQt5.QtWidgets import QApplication
from browser import Browser

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())