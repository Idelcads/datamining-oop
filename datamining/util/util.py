import os
import json
import pickle, sys

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

        if self._type =='pkl_densepose':
            f = open(path + '/' + name , 'rb')
            if 'detectron2/projects/DensePose' in os.getcwd():
                print(os.getcwd())
                sys.path.append(os.getcwd())
            else:
                sys.path.append(os.getcwd() + "/detectron2/projects/DensePose/")
                print(os.getcwd())
            self._data = pickle.load(f)

