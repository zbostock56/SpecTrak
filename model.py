class Model:
    def __init__(self):
        self._data = "Hello, MVC!"

    def get_data(self):
        return self._data

    def set_data(self, value):
        self._data = value
