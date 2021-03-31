## Installation

### Requirements
* Nvidia device with CUDA (for AlphaPose)
* Python 3.6+
* Cython
* PyTorch 1.5+
* numpy 1.19.5, matplotlib, open-cv 
* Linux

For more details on the libraries used please check [LIB.md](./LIB.md)

### Global installation: part 1
* conda create --prefix ./venv -y python=3.6
* conda activate ./venv
* conda install pytorch torchvision torchaudio cudatoolkit=11.1 numpy==1.19.5 -c pytorch -c conda-forge\
**need to specify numpy version here else, numpy conflit version will appear with detectron2**
* pip install flickrapi yacs natsort
* pip install -U albumentations
* conda install -c conda-forge dominate
* conda install scipy scikit-image tqdm
* pip install opencv-python


### AlphaPose Install: part 2
* git clone https://github.com/MVIG-SJTU/AlphaPose.git \
**follow then the installation instructions provided by AlphaPose: [AlphaPose/INSTALL.md](https://github.com/MVIG-SJTU/AlphaPose/blob/master/docs/INSTALL.md)** \
\
**don't forget to download model for AlphaPose: [MODEL_ZOO.md](https://github.com/MVIG-SJTU/AlphaPose/blob/master/docs/MODEL_ZOO.md)**

* For Bbox, `Fast Pose (DUC) - Resnet152 - from MSCOCO DATASET`
* For Pose Estimation, `Fast Pose - Resnet50 - from Halpe dataset` both 26 and 136 keypoints

You can also follow the script i used to install on my machine:
```
- cd AlphaPose
- git pull origin pull/592/head
- export PATH=/usr/local/cuda/bin/:$PATH
- export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:$LD_LIBRARY_PATH
- python -m pip install cython
- sudo apt-get install libyaml-dev
- pip install cython_bbox
- pip install easydict
- sudo apt-get install locales
- pip install pycocotools
- Download the object detection model manually: yolov3-spp.weights. Place it into detector/yolo/data

- python setup.py build develop
- python setup.py build develop (second times needed to finish the build)
```

### Detectron2 (DensePose) Install: part 3
* git clone https://github.com/facebookresearch/detectron2.git \
* pip install av
* cd detectron2\
**follow then the installation instructions provided by Facebook Detectron2: [Dectectron2/INSTALL.md](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md)** \
\
**don't forget to download model for DensePose: [ModelZoo.md](https://github.com/facebookresearch/detectron2/blob/master/projects/DensePose/doc/DENSEPOSE_IUV.md#ModelZoo)**

* [R_50_FPN_DL_s1x.pkl](https://dl.fbaipublicfiles.com/densepose/densepose_rcnn_R_50_FPN_DL_s1x/165712097/model_final_0ed407.pkl) then rename it densepose_rcnn_R_50_FPN_DL_s1x.pkl and put it on folder detectron2/projects/DensePose/checkpoints/
* [densepose_rcnn_R_50_FPN_DL_s1x.yaml](https://github.com/facebookresearch/detectron2/blob/master/projects/DensePose/configs/densepose_rcnn_R_50_FPN_DL_s1x.yaml) and put it on folder detectron2/projects/DensePose/configs


You can also follow the script i used to install on my machine:
```
- python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.8/index.html
```
