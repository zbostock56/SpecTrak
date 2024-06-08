class Model:
    """
    The Model class handles the data logic of the application.
    """

    def __init__(self):
        """
        Initializes the Model class.
        Sets the initial data value.
        """
        self._data = "Hello, MVC!"

    def get_data(self):
        """
        Gets the current data value.

        Returns:
            str: The current data value.
        """
        return self._data

    def set_data(self, value):
        """
        Sets the data value.

        Args:
            value (str): The new data value.
        """
        self._data = value