
class Data():
    def __init__(self, id: int, name: str, type_data: str, path: str):
        self._id = id
        self._name = name
        self._type_data = type_data
        self._path = path
        self._binary = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def type_data(self):
        return self._type_data

    @property
    def path(self):
        return self._path

    @property
    def binary(self):
        return self._binary

    @binary.setter
    def binary(self, value):
        self._binary = value