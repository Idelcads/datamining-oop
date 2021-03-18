from .data_loader import DataLoader
from datamining.data.data import Data
from flickrapi import FlickrAPI
from datamining.util.util import mkdirs
import os
import requests
import numpy as np

SIZES_LIST = np.array([4096,3072,2048,1600,1024,800,640,400,320,240,100])
SIZES_URL = ["url_4k", "url_3k", "url_k", "url_h", "url_b",
    "url_c", "url_z", "url_w", "url_n", "url_m", "url_t", "url_q", "url_s"]  # listed by order of preference

class FlickrLoader(DataLoader):
    def __init__(self, key: str, secret: str, keywords: list, count: int, min_size: int, max_size:int, orig_size: str, dataname: str, rawFolder: str):
        self._flickr = FlickrAPI(key, secret)
        self._keywords = keywords
        self._count = count
        self._dataname = dataname
        self._rawFolder = rawFolder
        self._index = 0

        self._sizes = []

        ind_min, ind_max = np.array(np.where(SIZES_LIST > min_size-1)), np.array(np.where(SIZES_LIST < max_size+1))
        if orig_size == 'yes':
            self._sizes = ["url_o"]
        else:
            for i in reversed(range(len(SIZES_LIST))):
                if (i in ind_min[0] and i in ind_max[0]):
                    self._sizes.append(SIZES_URL[i]) # listed by order of preference from the smallest to largest size
        if self._sizes==[]:
            raise ValueError("possible sizes values are 4096,3072,2048,1600,1024,800,640,400,320,240,100")

    def load(self):
        datas = []
        i = 1
        for keyword in self._keywords:

            if i == len(self._keywords):
                count_keyword = self._count - int(self._count / len(self._keywords)) * (i - 1)           
            else:
                count_keyword = int(self._count / len(self._keywords))
                
            urls = self.__get_urls(keyword, count_keyword)

            path = os.path.join('datasets', self._dataname, self._rawFolder)
            self.__download_images(urls, path, datas)
            i += 1
        return datas
    
    def __download_images(self, urls, path, datas):
        mkdirs(path)  # makes sure path exists

        for url in urls:
            ext = url.split("/")[-1][-4:]
            image_path = os.path.join(path, str(self._index) + ext)

            if not os.path.isfile(image_path):  # ignore if already downloaded TODO save url in txt img like id:url, and don't redownload if already in this file
                response=requests.get(url,stream=True)

                with open(image_path,'wb') as outfile:
                    outfile.write(response.content)
                    data = Data(self._index, str(self._index) + ext, "IMAGE", image_path)
                    datas.append(data)
            self._index += 1


    def __get_url(self, photo):
        for i in range(len(self._sizes)):
            url = photo.get(self._sizes[i])
            if url:  # if url is None try with the next size
                return url

    def __get_photos(self, image_tag):
        extras = ','.join(self._sizes)
        photos = self._flickr.walk(text=image_tag,
                                extras=extras,  # get the url for the original size image
                                privacy_filter=1,  # search only for public photos
                                per_page=50,
                                sort='relevance')
        return photos

    def __get_urls(self, image_tag, max):
        photos = self.__get_photos(image_tag)
        counter=0
        urls=[]

        for photo in photos:
            if counter < max:
                url = self.__get_url(photo)  # get preffered size url
                if url:
                    urls.append(url)
                    counter += 1
                # if no url for the desired sizes then try with the next photo
            else:
                break

        return urls

    


