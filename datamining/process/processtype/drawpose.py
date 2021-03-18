import random
import cv2
from matplotlib import pyplot as plt
import albumentations as A
import os, re
import argparse
import numpy as np
from datamining.data.dataloader.data_loader import DataLoader
from datamining.data.data import Data
from datamining.util.coloralpha import ColorAlpha
import os, re
from statistics import mean

class DrawPose():
    def __init__(self,config,alphapred):
        self._inputpath = os.path.join(os.getcwd(),'datasets', config.DATASET.NAME, config.POSE_ESTIMATION.PATH_PROCESS)
        self._inputfolder = config.POSE_ESTIMATION.PATH_PROCESS
        self._datasetname = config.DATASET.NAME
        self._savergb, self._saveblack, self._saveother = config.POSE_ESTIMATION.SAVE_RGB, config.POSE_ESTIMATION.SAVE_BLACK, config.POSE_ESTIMATION.SAVE_OTHER
        self._pathother = config.POSE_ESTIMATION.PATH_OTHER
        self._thickness_lines = config.POSE_ESTIMATION.DRAW_THICKNESS_LINES
        self._thickness_points = config.POSE_ESTIMATION.DRAW_THICKNESS_POINTS
        self._model = config.POSE_ESTIMATION.MODEL
        self._tresh = config.POSE_ESTIMATION.TRESH
        self._alphapred = alphapred._alphapred
        self._only_one = config.POSE_ESTIMATION.ONLY_ONE
        self._color = ColorAlpha(self._model)
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
        datas_black, datas_other = [], []
        for image in datas:
            num_iter += 1
            img_name = image._name
            for image_alphalabel in self._alphapred:
                if img_name == image_alphalabel[0]._image_id:
                    i=0
                    #read the original image
                    if len(image.binary) > 0:
                        original_image = image.binary
                    else:
                        original_image = cv2.imread(image.path, cv2.IMREAD_UNCHANGED)
                    heigth_org, width_org = original_image.shape[0:2]
                    try:
                        channel = original_image.shape[2]
                    except:
                        channel = 0
                    # initialise new image rgb, black and other
                    new_img_rgb = original_image
                    if self._saveblack == 'yes':
                        new_img_black = cv2.imread(image.path, cv2.IMREAD_UNCHANGED)
                        new_img_black[:] = 0 
                    if self._saveother == 'yes':
                        new_img_other = cv2.imread(self._pathother + image._name, cv2.IMREAD_UNCHANGED)
                    #Draw Pose Estimation in function of number of prediction
                    for label in image_alphalabel:
                        #Read keypoints position and confidence score:
                        keypoints = label._keypoints
                        x, y = keypoints._x, keypoints._y 
                        keypoints_len, confidence = keypoints._len, keypoints._confidence
                        
                        #Draw keypoints and lines:
                        if self._savergb == 'yes':
                            new_img_rgb = draw_keypoints(self._color._pointcolor, self._color._pair, new_img_rgb, x, y, confidence, self._thickness_points, self._tresh, self._model)
                            new_img_rgb = draw_lines(self._color._linecolor, self._color._pair, new_img_rgb, x, y, confidence, self._thickness_lines, self._tresh, self._model)
                        if self._saveblack == 'yes':
                            new_img_black = draw_keypoints(self._color._pointcolor, self._color._pair, new_img_black, x, y, confidence, self._thickness_points, self._tresh, self._model)
                            new_img_black = draw_lines(self._color._linecolor, self._color._pair, new_img_black, x, y, confidence, self._thickness_lines, self._tresh, self._model)
                        if self._saveother == 'yes':
                            try:
                                new_img_other = draw_keypoints(self._color._pointcolor, self._color._pair, new_img_other, x, y, confidence, self._thickness_points, self._tresh, self._model)
                                new_img_other = draw_lines(self._color._linecolor, self._color._pair, new_img_other, x, y, confidence, self._thickness_lines, self._tresh, self._model)
                            except:
                                print('\033[91m','POSE_ESTIMATION : PATH_OTHER for other images is wrong or other images don''t have the same name than original ones.','\033[0m')

                        #write new image datas, datas_black and datas_other
                        if i ==0: #in this case we write the first prediction draw on image
                            # RGB images write on datas
                            self._index = image._id
                            if self._savergb == 'yes':
                                image.binary = new_img_rgb
                                new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'pose_estimation/' + self._inputfolder, 'rgb')
                                image._path= os.path.join(new_folder , img_name)
                            # black images write on new datas
                            if self._saveblack == 'yes':
                                new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'pose_estimation/' + self._inputfolder, 'black')
                                new_path = os.path.join(new_folder , img_name)
                                datas_b = Data(self._index, img_name, "IMAGE", new_path)
                                datas_b.binary = new_img_black
                                datas_black.append(datas_b)
                                # other images write on new datas
                            if self._saveother == 'yes':
                                new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'pose_estimation/' + self._inputfolder, 'other')
                                new_path = os.path.join(new_folder , img_name)
                                datas_o = Data(self._index, img_name, "IMAGE", new_path)
                                datas_o.binary = new_img_other
                                datas_other.append(datas_o)
                            i +=1
                        elif i != 0 and self._only_one == 'no': #in this case we write the other prediction on image (condition sur only_one)
                            # RGB images write on datas
                            self._index = image._id
                            if self._savergb == 'yes':
                                image.binary = new_img_rgb
                                new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'pose_estimation/' + self._inputfolder, 'rgb')
                                image._path= os.path.join(new_folder , img_name)
                            # black images write on new datas
                            if self._saveblack == 'yes':
                                new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'pose_estimation/' + self._inputfolder, 'black')
                                new_path = os.path.join(new_folder , img_name)
                                datas_b = Data(self._index, img_name, "IMAGE", new_path)
                                datas_b.binary = new_img_black
                                datas_black.append(datas_b)
                            # other images write on new datas
                            if self._saveother == 'yes':
                                new_folder = os.path.join(os.getcwd(),'datasets',self._datasetname, 'pose_estimation/' + self._inputfolder, 'other')
                                new_path = os.path.join(new_folder , img_name)
                                datas_o = Data(self._index, img_name, "IMAGE", new_path)
                                datas_o.binary = new_img_other
                                datas_other.append(datas_o)
                            i +=1


        return datas, datas_black, datas_other
    
def draw_keypoints(color, pair, img, x, y, confidence, thickness, tresh, model):
    # Draw keypoints 
    thick = thickness
    if thick != 0:
        color = color._p_color
        vis_thres = tresh*0.1 if model == 136 else tresh
        for n in range(len(confidence)):
            if confidence[n] <= vis_thres:
                continue
            cor_x, cor_y = int(x[n]), int(y[n])
            bg = img
            # if n < 26 or n > 93:
            if n < len(color):
                cv2.circle(bg, (int(cor_x), int(cor_y)), 4, color[n], 1*thick)
            else:
                cv2.circle(bg, (int(cor_x), int(cor_y)), 4, (255,255,255), 1*thick)
            # Now create a mask of logo and create its inverse mask also
            transparency = 1
            img = cv2.addWeighted(bg, transparency, img, 1 - transparency, 0)

    return img

def draw_lines(color, pair, img, x, y, confidence, thickness, tresh, model):
    # Draw limbs
    part_line = {}
    thick = thickness
    if thick != 0:
        color = color._l_color
        pair = pair._l_pair
        vis_thres = tresh*0.1 if model == 136 else tresh
        for n in range(len(confidence)):
            if confidence[n] <= vis_thres:
                continue
            cor_x, cor_y = int(x[n]), int(y[n])
            part_line[n] = (int(cor_x), int(cor_y))

        for i, (start_p, end_p) in enumerate(pair):
            if start_p in part_line and end_p in part_line:
                start_xy = part_line[start_p]
                end_xy = part_line[end_p]
                bg = img
                X = (start_xy[0], end_xy[0])
                Y = (start_xy[1], end_xy[1])
                # if i < 24 or i > 83 :
                if i < len(color):
                    cv2.line(bg, start_xy, end_xy, color[i], 1*thick)
                else:
                    cv2.line(bg, start_xy, end_xy, (255,255,255), 1*thick)
                transparency = 1
                img = cv2.addWeighted(bg, transparency, img, 1 - transparency, 0)
        
    return img
