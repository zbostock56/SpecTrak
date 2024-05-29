import sys
from PyQt6.QtWidgets import QApplication
from model import Model
from view import View

class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.model = Model()
        self.view = View()
        self.view.button.clicked.connect(self.update_model)

    def show_view(self):
        self.view.show()

    def update_model(self):
        new_data = self.view.get_input_text()
        self.model.set_data(new_data)
        self.view.set_label_text(self.model.get_data())

    def run(self):
        self.show_view()
        sys.exit(self.app.exec())

if __name__ == '__main__':
    controller = Controller()
    controller.run()
