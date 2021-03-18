import cv2

class Crop():
    def __init__(self, size):
        self._size = size
        
    def process(self, datas):
        for data in datas:
            if len(data.binary) > 0:
                image = data.binary
            else:
                image = cv2.imread(data.path, cv2.IMREAD_UNCHANGED)

            try:
                heigth, width = image.shape[:2]

                if width > self._size:
                    x = int((width - self._size) / 2)
                    crop_img = image[::, x:x+self._size]
                else:
                    border_v = 0
                    if (heigth-width) % 2 == 0:
                        border_h1 = int((heigth-width)/2)
                        border_h2 = int((heigth-width)/2)
                    else:
                        border_h1 = int((heigth-width)/2) + 1
                        border_h2 = int((heigth-width)/2)
                    
                    black = [0,0,0]
                    crop_img = cv2.copyMakeBorder(image, border_v, border_v, border_h1, border_h2, cv2.BORDER_CONSTANT, value=black) 

                data.binary = crop_img
            except:
                print("[CROP] An exception occurred : ", data.path, "not exists")
                datas.remove(data)

        return datas
        