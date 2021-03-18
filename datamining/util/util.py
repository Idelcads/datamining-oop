import os
import json

def mkdirs(paths):
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


class ReadFile():
    def __init__(self, type, path, name):
        self._type = type
        self._name = name
        self._InputPath = path

        if self._type =='json':
            with open(path + '/' + name) as f:
                self._data = json.load(f)