import os
import json


class AlphaPred():
    def __init__(self, jsonfile):
        self._image_id = []
        n = jsonfile._data[0]['image_id']
        size=0
        for jsondata in jsonfile._data:
            if jsondata['image_id'] != n:
                n = jsondata['image_id']
                size+=1
        self._alphapred = AlphaPred.init_list_of_objects(size+1)

        n = jsonfile._data[0]['image_id']
        i = 0
        for jsondata in jsonfile._data:
            if jsondata['image_id'] == n:
                self._alphalabel = AlphaLabels(jsondata)
                self._alphapred[i].append(self._alphalabel)
            else:
                n = jsondata['image_id']
                i+=1
                self._alphalabel = AlphaLabels(jsondata)
                self._alphapred[i].append(self._alphalabel)
        a=0
    
    def init_list_of_objects(size):
        list_of_objects = list()
        for i in range(0,size):
            list_of_objects.append( list() ) #different object reference each time
        return list_of_objects

class AlphaLabels():
    def __init__(self, jsondata):
        self._keypoints = Keypoints(jsondata['keypoints'])
        self._boxes = Boxes(jsondata['box'], jsondata['score'], jsondata['category_id'])
        self._image_id = jsondata['image_id']

class Keypoints():
    def __init__(self, val):
        self._len = int(len(val)/3)
        self._confidence = []
        self._x = []
        self._y = []
        for i in range(0,len(val)-2,3):
            self._confidence.append(val[i+2])
            self._x.append(val[i])
            self._y.append(val[i+1])
 
class Boxes():
    def __init__(self, box, score, cat):
        self._score = score 
        self._x = box[0]
        self._y = box[1]
        self._width = box[2]
        self._heigth = box[3]
        self._category = cat