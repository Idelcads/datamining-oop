import random
import cv2
from matplotlib import pyplot as plt
import albumentations as A
import os, re
import argparse
import numpy as np
from datamining.data.dataloader.data_loader import DataLoader
from datamining.data.data import Data
import os, re
from statistics import mean

class CropBox():
    def __init__(self,config,alphapred):
        self._inputpath = os.path.join(os.getcwd(),'datasets', config.DATASET.NAME, config.BBOX.PATH_PROCESS)
        self._box_min_size = config.BBOX.MIN_SIZE
        self._inputfolder = config.BBOX.PATH_PROCESS
        self._datasetname = config.DATASET.NAME
        self._tresh = config.BBOX.TRESH
        self._alphapred = alphapred._alphapred
        self._only_one = config.BBOX.ONLY_ONE
        

    def process(self, datas):
        datas = datas
        self._index, original_len = len(datas), len(datas)
        num_iter = 0
        for image in datas:
            num_iter += 1
            img_name = image._name
            for image_alphalabel in self._alphapred:
                if img_name == image_alphalabel[0]._image_id:
                    i=0
                    #read the image
                    if len(image.binary) > 0:
                        original_image = image.binary
                    else:
                        original_image = cv2.imread(image.path, cv2.IMREAD_UNCHANGED)
                        heigth_org, width_org = original_image.shape[0:2]
                    #apply box extraction in function of number of estimation 
                    for label in image_alphalabel:
                        #extract image
                        new_img =  []
                        new_img_name = CropBox.new_name(img_name,i)
                        box = label._boxes
                        x, y = int(box._x), int(box._y)
                        heigth, width = int(box._heigth), int(box._width)
                        score = box._score
                        x_end, y_end = CropBox.end(width_org,x+width), CropBox.end(heigth_org,y+heigth)
                        confidence_keypoints = label._keypoints._confidence
                        try:
                            new_img = original_image[y:y_end,x:x_end,0:3]
                        except:
                            new_img = original_image[y:y+heigth,x:x+width]

                        if (int((new_img.shape[0]*100)/heigth_org) > self._box_min_size or int((new_img.shape[1]*100)/width_org) > self._box_min_size):# condition taille de la box
                            if score > self._tresh: # condition sur la condidence : cas sur la moyenne
                            # if confidence_keypoints[0] > self._tresh and confidence_keypoints[-1] > self._tresh # condition sur la condidence : cas sur la 1er et last value
                                #write new image on datas
                                if i ==0: #in this case we can just replace original data
                                    image.binary = new_img
                                    image._name = new_img_name
                                    new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'bbox/' + self._inputfolder)
                                    image._path= os.path.join(new_folder , new_img_name)
                                    i +=1
                                elif i != 0 and self._only_one!= 'yes': #condition sur only_one
                                    # ajouter une nouvelle data avec un nouvel index 
                                    self._index += 1
                                    new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'bbox/' + self._inputfolder)
                                    new_path = os.path.join(new_folder , new_img_name)
                                    new_data = Data(self._index, new_img_name, "IMAGE", new_path)
                                    new_data.binary = new_img
                                    datas.append(new_data)
                                    i+=1
            # condition to leave the initial for loop because we increase size of datas
            if num_iter >= original_len:
                break

        return datas

    def new_name(name_img,index):
        if name_img.endswith('.jpg'):
            new_name = name_img[:-4] + '_' + str(index) + ('.jpg')
        elif name_img.endswith('.png'):
            new_name = name_img[:-4] + '_' + str(index) + ('.png')
        elif name_img.endswith('.jpeg'):
            new_name = name_img[:-5] + '_' + str(index) + ('.jpeg')
        return new_name

    def end(org,new):
        if new <=org:
            return new
        else:
            return org
