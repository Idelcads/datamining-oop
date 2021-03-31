import random
import cv2
from matplotlib import pyplot as plt
import albumentations as A
import os, re
import argparse
import numpy as np
from datamining.data.dataloader.data_loader import DataLoader
from datamining.data.data import Data
from datamining.util.colordense import ColorDense
import os, re
from statistics import mean

class DrawDensePose():
    def __init__(self,config,densepred):
        self._inputpath = os.path.join(os.getcwd(),'datasets', config.DATASET.NAME, config.DENSEPOSE.PATH_PROCESS)
        self._inputfolder = config.DENSEPOSE.PATH_PROCESS
        self._datasetname = config.DATASET.NAME
        self._savergb, self._saveblack, self._savegreen = config.DENSEPOSE.SAVE_RGB, config.DENSEPOSE.SAVE_BLACK, config.DENSEPOSE.SAVE_GREEN

        self._tresh = config.DENSEPOSE.TRESH
        self._densepred = densepred._densepred
        self._only_one = config.DENSEPOSE.ONLY_ONE
        self._color = ColorDense()
        self._color = self._color._color
        #write name of the output folder
        pos = self._inputfolder.find('/')
        if pos !=-1:
            self._inputfolder = self._inputfolder[0:pos] + '_' + self._inputfolder[pos+1:]
        else:
            self._inputfolder = self._inputfolder

    def process(self, datas):
        datas = datas
        original_len = len(datas)
        num_iter = 0
        datas_black, datas_green = [], []
        for image in datas:
            print('len data : ', len(datas))
            print('num iter : ', num_iter)
            num_iter += 1
            img_name = image._name
            for image_denselabel in self._densepred:
                img_name2 = image_denselabel[0]._image_name[len(self._inputpath)+1:]
                if img_name ==  img_name2:
                # if img_name in image_denselabel[0]._image_name:
                    new_img_rgb, new_img_black, new_img_green =load_image(image, image_denselabel, self._saveblack, self._savegreen)
                    i=0
                    print(image.path)
                    #Search of the prediction with biggest area for only_one condition
                    area = []
                    for label in image_denselabel:
                        #variable to store area of all extracted box
                        box = label._boxes
                        heigth, width = int(box._heigth), int(box._width)
                        area.append(heigth*width)

                    #Draw Pose Estimation in function of number of prediction
                    for label in image_denselabel:
                        box = label._boxes
                        heigth, width = int(box._heigth), int(box._width)
                        area_img = heigth*width
                        #Read box position, mask values and confidence score:
                        mask = label._mask
                        x_min, y_min = box._x, box._y 
                        x_max, y_max = x_min+width, y_min+heigth
                        score = label._score
                        if area_img == max(area) and self._only_one == 'yes': #draw only prediction with biggest area
                            #Draw mask:
                            if self._savergb == 'yes' and score >= self._tresh:
                                new_img_rgb = draw_masks(self._color, new_img_rgb, [x_min, x_max], [y_min,y_max], mask)
                            if self._saveblack == 'yes' and score >= self._tresh:
                                new_img_black = draw_masks(self._color, new_img_black, [x_min, x_max], [y_min,y_max], mask)
                            if self._savegreen == 'yes'and score >= self._tresh:
                                new_img_green = draw_masks(self._color, new_img_green, [x_min, x_max], [y_min,y_max], mask)
                        elif self._only_one == 'no': #draw all prediction 
                            #Draw masks:
                            if self._savergb == 'yes' and score >= self._tresh:
                                new_img_rgb = draw_masks(self._color, new_img_rgb, [x_min, x_max], [y_min,y_max], mask)
                            if self._saveblack == 'yes' and score >= self._tresh:
                                new_img_black = draw_masks(self._color, new_img_black, [x_min, x_max], [y_min,y_max], mask)
                            if self._savegreen == 'yes' and score >= self._tresh:
                                new_img_green = draw_masks(self._color, new_img_green, [x_min, x_max], [y_min,y_max], mask)
                    #write new image datas, datas_black and datas_other
                    # RGB images write on datas
                    self._index = image._id
                    if self._savergb == 'yes':
                        image.binary = new_img_rgb
                        new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'densepose/' + self._inputfolder, 'rgb')
                        image._path= os.path.join(new_folder , img_name)
                    # black images write on new datas
                    if self._saveblack == 'yes':
                        new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'densepose/' + self._inputfolder, 'black')
                        new_path = os.path.join(new_folder , img_name)
                        datas_b = Data(self._index, img_name, "IMAGE", new_path)
                        datas_b.binary = new_img_black
                        datas_black.append(datas_b)
                    # other images write on new datas
                    if self._savegreen == 'yes':
                        new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'densepose/' + self._inputfolder, 'green')
                        new_path = os.path.join(new_folder , img_name)
                        datas_g = Data(self._index, img_name, "IMAGE", new_path)
                        datas_g.binary = new_img_green
                        datas_green.append(datas_g)
                    i +=1


        return datas, datas_black, datas_green
    
def draw_masks(color, img, x, y, mask):
    # Draw keypoints 
    for i in range(1,27):
        val = i
        paint = color[i]
        box_img = img[y[0]:y[1],x[0]:x[1],:]
        index_v = np.where(mask==val)
        try:
            box_img[index_v[0],index_v[1],0:3] = paint
        except:
            pass
    return img

def load_image(image, image_denselabel, saveblack, savegreen):
    #read the original image
    new_img_rgb, new_img_black, new_img_green = [], [], []
    print(image_denselabel[0]._image_name)
    if len(image.binary) > 0:
        original_image = image.binary
    else:
        original_image = cv2.imread(image_denselabel[0]._image_name, cv2.IMREAD_UNCHANGED)
    heigth_org, width_org = original_image.shape[0:2]
    try:
        channel = original_image.shape[2]
    except:
        channel = 0
    # initialise new rgb image with condition to delete 4th channel
    if channel < 4:
        new_img_rgb = original_image
    else:
        new_img_rgb = original_image[:,:,0:3]
    # initialise new black image with condition to delete 4th channel
    if saveblack == 'yes':
        original_black = cv2.imread(image_denselabel[0]._image_name, cv2.IMREAD_UNCHANGED)
        if channel < 4:
            new_img_black = original_black
            new_img_black[:] = 0 
        else:
            new_img_black = original_black[:,:,0:3]
            new_img_black[:] = 0 
    # initialise new other image with condition to delete 4th channel
    if savegreen == 'yes':
        original_green = cv2.imread(image_denselabel[0]._image_name, cv2.IMREAD_UNCHANGED)
        if channel < 4:
            new_img_green = original_green
        else:
            new_img_green = original_green[:,:,0:3]
        try:
            new_img_green[:,:,0:3] = [0,255,0]
        except:
            pass
    return new_img_rgb, new_img_black, new_img_green