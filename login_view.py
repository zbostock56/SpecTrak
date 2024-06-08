from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QRadioButton
from PyQt6.uic import loadUi

class LoginView(QMainWindow):
    def __init__(self):
        super(LoginView, self).__init__()
        loadUi('login.ui', self)
        self.usernameInput = self.findChild(QLineEdit, 'usernameInput')
        self.passwordInput = self.findChild(QLineEdit, 'passwordInput')
        self.remotePathInput = self.findChild(QLineEdit, 'remotePathInput')
        self.connectButton = self.findChild(QPushButton, 'connectButton')
        self.radioPassword = self.findChild(QRadioButton, 'radioPassword')
        self.radioKey = self.findChild(QRadioButton, 'radioKey')
