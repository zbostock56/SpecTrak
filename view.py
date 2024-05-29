from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit

class View(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setWindowTitle("SpecTrak")

        self.label = QLabel('Data:')
        self.layout.addWidget(self.label)

        self.input = QLineEdit()
        self.layout.addWidget(self.input)

        self.button = QPushButton('Update')
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def get_input_text(self):
        return self.input.text()

    def set_label_text(self, text):
        self.label.setText(f'Data: {text}')

    def show_full_screen(self):
        self.showFullScreen()
