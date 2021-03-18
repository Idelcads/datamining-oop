## Installation

### Requirements
* Nvidia device with CUDA (for AlphaPose)
* Python 3.6+
* Cython
* PyTorch 1.5+
* numpy, matplotlib, open-cv 
* Linux

For more details on the libraries used please check [LIB.md](./LIB.md)

### Global installation: part 1
* conda create --prefix ./venv -y python=3.6
* conda activate ./venv

* conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c conda-forge
* pip install flickrapi
* pip install yacs
* pip install -U albumentations
* conda install -c conda-forge dominate
* conda install scipy scikit-image
* conda install tqdm
* pip install natsort
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
- export PATH=/usr/local/cuda/bin/:$PATH
- export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:$LD_LIBRARY_PATH
- python -m pip install cython
- sudo apt-get install libyaml-dev
- pip install cython_bbox
- pip install easydict
- sudo apt-get install locales

- python setup.py build develop
```