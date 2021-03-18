from .data_loader import DataLoader
from datamining.data.data import Data
import os, re

class LocalLoader(DataLoader):
    def __init__(self, dataname: str, rawFolder: str):
        self._dataname = dataname
        self._rawFolder = rawFolder
        self._index = 0

    def load(self):
        datas = []

        path = os.path.join('datasets', self._dataname, self._rawFolder)

        filelist=self.__sorted_alphanumeric(os.listdir(path))


        for image in filelist[:]:

            if not(image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg")):
                filelist.remove(image)
            else:
                data = Data(self._index, image, "IMAGE", path + '/' + image)
                datas.append(data)
                self._index += 1
        return datas

    def __sorted_alphanumeric(self, data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(data, key=alphanum_key)
    

    


