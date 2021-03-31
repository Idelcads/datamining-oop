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

class DensePred():
    def __init__(self, pklfile):
        self._image_id = []
        size=len(pklfile._data)
        self._densepred = DensePred.init_list_of_objects(size)
        i = 0
        for pkldata in pklfile._data: # For each images
            for pred_it in range(len(pkldata['pred_boxes_XYXY'])): #For each prefiction on the image
                # self._denselabel = DenseLabels(pkldata['scores'][pred_it], pkldata['pred_boxes_XYXY'][pred_it], pkldata['pred_densepose'][pred_it], pkldata['file_name'])
                # self._densepred[i].append(self._denselabel)
                self._densepred[i].append(DenseLabels(pkldata['scores'][pred_it], pkldata['pred_boxes_XYXY'][pred_it], pkldata['pred_densepose'][pred_it], pkldata['file_name']))
            i+=1
        a=0
    
    def init_list_of_objects(size):
        list_of_objects = list()
        for i in range(0,size):
            list_of_objects.append( list() ) #different object reference each time
        return list_of_objects

class DenseLabels():
    def __init__(self, score, boxes, mask, name):

        box_dense_to_alpha = DenseLabels.box_translate(boxes)
        self._boxes = Boxes(box_dense_to_alpha, score, 0)

        self._image_name = name
        self._score = score.numpy()

        mask = DenseLabels.mask_translate(mask)
        self._mask = mask

    
    def box_translate(boxes): # needed to transform xmax and ymax into width and heigth
        xmin, ymin, xmax, ymax = int(boxes[0]), int(boxes[1]), int(boxes[2]), int(boxes[3])
        boxes = [xmin, ymin, xmax-xmin, ymax-ymin]
        return boxes

    def mask_translate(mask): # needed to transform tensor gpu array into numpy array
        try:
            mask = mask.labels.numpy()
        except:
            mask = mask.labels.cpu()
            mask = mask.numpy()
        return mask