import random
import cv2
from matplotlib import pyplot as plt
import albumentations as A
import os, re
import argparse
import numpy as np

class Resize():
    def __init__(self, config):
        self._size = config.RESIZE.SIZE
        pos = self._size.find('x')
        self._new_width, self._new_heigth = int(self._size[0:pos]), int(self._size[pos+1:])
        self._interpolation = config.RESIZE.INTERPOLATION

    def process(self, datas):
        for data in datas:
            if len(data.binary) > 0:
                original_image = data.binary
            else:
                original_image = cv2.imread(data.path, cv2.IMREAD_UNCHANGED)
            try:
                original_heigth, original_width = original_image.shape[:2]
                try:
                    channel = original_image.shape[2]
                except:
                    channel = 0
                self._final_heigth, self._final_width = Resize.compute_final_size(self._new_width, self._new_heigth, original_heigth, original_width)

                resized_image = np.zeros((self._new_heigth,self._new_width,channel),dtype=np.uint8)
                transform = A.ReplayCompose([A.Resize (self._final_heigth, self._final_width, interpolation=self._interpolation, always_apply=True)])
                transformed = transform(image=original_image)
                image_transform = transformed['image']

                # Put images on the middle of the final image
                delta_h, delta_w = int((self._new_heigth - self._final_heigth)/2), int((self._new_width - self._final_width)/2)
                resized_image[delta_h:self._final_heigth+delta_h, delta_w:self._final_width+delta_w,:] = image_transform[:,:,:]

                data.binary = resized_image

            except:
                print("[RESIZE] An exception occurred : ", data.path, "not exists")
                datas.remove(data)
            
        return datas

    def compute_final_size (new_width, new_heigth, original_heigth, original_width): 
            ratio_heigth = max(new_heigth,original_heigth)/min(new_heigth,original_heigth)
            ratio_width = max(new_width,original_width)/min(new_width,original_width)
            ind = 0
            if ratio_heigth <= ratio_width:
                    final_heigth = new_heigth
                    final_width = int((new_heigth/original_heigth)*original_width)
                    ind = 1
            else:
                    final_width = new_width
                    final_heigth = int((new_width/original_width)*original_heigth) 
                    ind = 2
            if final_width > new_width or final_heigth > new_heigth:
                    if ind ==1:
                            final_width = new_width
                            final_heigth = int((new_width/original_width)*original_heigth) 
                    elif ind == 2:
                            final_heigth = new_heigth
                            final_width = int((new_heigth/original_heigth)*original_width)
            return final_heigth, final_width
            
        