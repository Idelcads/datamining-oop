from .processtype.process_type import ProcessType
from .processtype.resize import Resize
from .processtype.cropbox import CropBox
from .processtype.drawpose import DrawPose
from .processtype.drawdensepose import DrawDensePose
from .processtype.crop import Crop
from datamining.util.util import mkdirs, ReadFile
from datamining.data.labels import AlphaPred, DensePred
import cv2
import os, shutil


import numpy as np
import torch

class ProcessServiceResizeCrop():
    def __init__(self, config):
        self._process_list = []
        self._process_dir = config.DATASET.RAW
        self._dataname = config.DATASET.NAME
        self._datas = None
        self._resize = config.PROCESS.RESIZE
        # self._crop = config.PROCESS.CROP

        if (config.PROCESS.RESIZE == 'yes'):
            self._process_dir = config.RESIZE.PATH_PROCESS
            resize = Resize(config)
            self._process_list.append(resize)

        # if (config.PROCESS.CROP != 0):
        #     crop = Crop(config.PROCESS.CROP)
        #     self._process_list.append(crop)

    def run(self, datas):
        self._datas = datas
        for process in self._process_list:
            self._datas = process.process(self._datas)
        
    def save(self):
        if self._resize == 'yes':
            pos = self._process_dir.find('/')
            if pos !=-1:
                name_folder_resize = self._process_dir[0:pos] + '_' + self._process_dir[pos+1:]
            else:
                name_folder_resize = self._process_dir
            path = os.path.join('datasets', self._dataname, 'resize', name_folder_resize)
            mkdirs(path)
            for data in self._datas:
                cv2.imwrite(path + '/' + data.name, data.binary)
        # elif self._resize == 'yes' and self._crop != 0:
        #     path = os.path.join('datasets', self._dataname, self._process_dir + '_resize_crop')
        #     mkdirs(path)
        #     for data in self._datas:
        #         cv2.imwrite(path + '/' + data.name, data.binary)
        # elif self._resize == 'no' and self._crop != 0:
        #     path = os.path.join('datasets', self._dataname, self._process_dir + '_crop')
        #     mkdirs(path)
        #     for data in self._datas:
        #         cv2.imwrite(path + '/' + data.name, data.binary)

class ProcessServiceAPI():
    def __init__(self, config):
        self._process_list = []
        self._process_dir = config.DATASET.RAW
        self._dataname = config.DATASET.NAME
        self._datas = None

    def run(self, datas):
        self._datas = datas
        for process in self._process_list:
            self._datas = process.process(self._datas)
        
    def save(self):
        self._status = 'OK'

class ProcessServiceAlphaBox():
    def __init__(self, config):
        self._process_list = []
        self._dataname = config.DATASET.NAME
        self._datas = None
        self._bbox = config.PROCESS.BBOX
        self._pose = config.PROCESS.POSE_ESTIMATION

        if (config.PROCESS.BBOX == 'yes'):
            self._case = 0 # cas BBOX
            self._process_dir = config.BBOX.PATH_PROCESS
            self._savepred = config.BBOX.SAVE_PRED
            self._vispred = config.BBOX.VIS_PRED

            # write command to launch AlphaPose
            from ..segment.alphapose.alphapose_mapper import AlphaPoseMapper
            mapper = AlphaPoseMapper(config,self._process_dir, self._case)
            mapper.run()

            # READ JSON contenue dans temp folder
            self._jsonfile = ReadFile('json', mapper._outputpath, 'alphapose-results.json' )
            self._alphapred = AlphaPred(self._jsonfile)

            # Crop box on images
            cropbox = CropBox(config, self._alphapred)

            # Delete temp file
            self._process_list.append(cropbox)


    def run(self, datas):
        self._datas = datas
        for process in self._process_list:
            self._datas = process.process(self._datas)
        
    def save(self):
        if self._bbox == 'yes':
            for data in self._datas:
                img_name = data.name
                path = data.path[:-len(img_name)]
                os.makedirs(path, exist_ok=True)
                try:
                    cv2.imwrite(path + img_name, data.binary)
                except:
                    pass
            # Save images and json which are in temp file if needed
            try:
                if self._vispred == 'yes':
                    path_temp = self._jsonfile._InputPath
                    path = path[:-1] + '_pred/'
                    try:
                        shutil.move(path_temp, path)
                    except:
                        pass
                # delete temp folder
                path_temp_rm = os.path.join('datasets', self._dataname, 'temp')
                shutil.rmtree(path_temp_rm)
            except:
                pass

class ProcessServiceDensePose():
    def __init__(self, config):
        self._process_list = []
        self._dataname = config.DATASET.NAME
        self._datas = None
        self._densepose = config.PROCESS.DENSEPOSE
 
        if (self._densepose == 'yes'):
            self._process_dir = config.DENSEPOSE.PATH_PROCESS

            # write command to launch AlphaPose
            from ..segment.detectron.detectron_mapper import DensePoseMapper
            mapper = DensePoseMapper(config,self._process_dir)
            mapper.run()

            # READ .pkl file 
            self._pklfile = ReadFile('pkl_densepose', mapper._outputpath, 'results.pkl' )
            self._densepred = DensePred(self._pklfile)
            
            # Draw DensePose Estimation on images
            drawdensepose = DrawDensePose(config, self._densepred)
            self._process_list.append(drawdensepose)
            
            # What to save
            self._savergb = config.DENSEPOSE.SAVE_RGB
            self._saveblack = config.DENSEPOSE.SAVE_BLACK
            self._savegreen = config.DENSEPOSE.SAVE_GREEN
            # OutputPath
            self._inputfolder = config.DENSEPOSE.PATH_PROCESS
            pos = self._inputfolder.find('/')
            if pos !=-1:
                self._inputfolder = self._inputfolder[0:pos] + '_' + self._inputfolder[pos+1:]
            else:
                self._inputfolder = self._inputfolder
            self._outputpath = os.path.join(os.getcwd(),'datasets',self._dataname, 'densepose/' + self._inputfolder)


    def run(self, datas):
        self._datas = datas
        for process in self._process_list:
            self._datas, self._datas_black, self._datas_green = process.process(self._datas)
        
    def save(self):
        if self._densepose == 'yes':
            # save rgb images
            if self._savergb == 'yes':
                glob_path = self._datas[0]._path[:-(len(self._datas[0]._name)+4)]
                for data in self._datas:
                    img_name = data.name
                    path = data.path[:-len(img_name)]
                    os.makedirs(path, exist_ok=True)
                    try:
                        cv2.imwrite(path + img_name, data.binary)
                    except:
                        pass
            # save black images
            if self._saveblack == 'yes':
                for data in self._datas_black:
                    img_name = data.name
                    path = data.path[:-len(img_name)]
                    os.makedirs(path, exist_ok=True)
                    try:
                        cv2.imwrite(path + img_name, data.binary)
                    except:
                        pass
            # save green images
            if self._savegreen == 'yes':
                for data in self._datas_green:
                    img_name = data.name
                    path = data.path[:-len(img_name)]
                    os.makedirs(path, exist_ok=True)
                    try:
                        cv2.imwrite(path + img_name, data.binary)
                    except:
                        pass
            # delete temp folder
            path_temp_rm = os.path.join('datasets', self._dataname, 'temp')
            shutil.rmtree(path_temp_rm)

class ProcessServiceAlphaPose():
    def __init__(self, config):
        self._process_list = []
        self._dataname = config.DATASET.NAME
        self._datas = None
        self._bbox = config.PROCESS.BBOX
        self._pose = config.PROCESS.POSE_ESTIMATION
 
        if (config.PROCESS.POSE_ESTIMATION == 'yes'):
            self._case = 1 # cas POSE ESTIMATION
            self._process_dir = config.POSE_ESTIMATION.PATH_PROCESS

            # write command to launch AlphaPose
            from ..segment.alphapose.alphapose_mapper import AlphaPoseMapper
            mapper = AlphaPoseMapper(config,self._process_dir, self._case)
            mapper.run()

            # READ JSON contenue dans temp folder
            self._jsonfile = ReadFile('json', mapper._outputpath, 'alphapose-results.json' )
            self._alphapred = AlphaPred(self._jsonfile)
            
            # Draw Pose Estimation on images
            drawpose = DrawPose(config, self._alphapred)

            # Delete temp file
            self._process_list.append(drawpose)
            
            # What to save
            self._savepred = config.POSE_ESTIMATION.VIS_PRED
            self._savergb = config.POSE_ESTIMATION.SAVE_RGB
            self._saveblack = config.POSE_ESTIMATION.SAVE_BLACK
            self._saveother = config.POSE_ESTIMATION.SAVE_OTHER
            self._vispred = config.POSE_ESTIMATION.VIS_PRED
            # OutputPath
            self._inputfolder = config.POSE_ESTIMATION.PATH_PROCESS
            pos = self._inputfolder.find('/')
            if pos !=-1:
                self._inputfolder = self._inputfolder[0:pos] + '_' + self._inputfolder[pos+1:]
            else:
                self._inputfolder = self._inputfolder
            self._outputpath = os.path.join(os.getcwd(),'datasets',self._dataname, 'pose_estimation/' + self._inputfolder)


    def run(self, datas):
        self._datas = datas
        for process in self._process_list:
            self._datas, self._datas_black, self._datas_other = process.process(self._datas)
        
    def save(self):
        if self._pose == 'yes':
            # save rgb images
            if self._savergb == 'yes':
                glob_path = self._datas[0]._path[:-(len(self._datas[0]._name)+4)]
                for data in self._datas:
                    img_name = data.name
                    path = data.path[:-len(img_name)]
                    os.makedirs(path, exist_ok=True)
                    try:
                        cv2.imwrite(path + img_name, data.binary)
                    except:
                        pass
            # save black images
            if self._saveblack == 'yes':
                for data in self._datas_black:
                    img_name = data.name
                    path = data.path[:-len(img_name)]
                    os.makedirs(path, exist_ok=True)
                    try:
                        cv2.imwrite(path + img_name, data.binary)
                    except:
                        pass
            # save other images
            if self._saveother == 'yes':
                for data in self._datas_other:
                    img_name = data.name
                    path = data.path[:-len(img_name)]
                    os.makedirs(path, exist_ok=True)
                    try:
                        cv2.imwrite(path + img_name, data.binary)
                    except:
                        pass
            # Save images and json which are in temp file if needed
            if self._vispred == 'yes':
                path_temp = self._jsonfile._InputPath
                path = os.path.join(self._outputpath, 'AlphaPose_Vis')
                try:
                    shutil.move(path_temp, path)
                except:
                    pass
            # delete temp folder
            path_temp_rm = os.path.join('datasets', self._dataname, 'temp')
            shutil.rmtree(path_temp_rm)