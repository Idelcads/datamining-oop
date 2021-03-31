import os
import torch

class DensePoseMapper():
    def __init__(self, config, path):

        self._inputpath = os.path.join(os.getcwd(),'datasets', config.DATASET.NAME, path)
        self._outputpath = os.path.join(os.getcwd(),'datasets', config.DATASET.NAME, 'temp/densepose')
        os.makedirs(self._outputpath, exist_ok=True)
        self._cmd = 'python apply_net.py dump configs/densepose_rcnn_R_50_FPN_DL_s1x.yaml checkpoints/densepose_rcnn_R_50_FPN_DL_s1x.pkl '\
            + self._inputpath + ' --output ' + self._outputpath + '/results.pkl -v'
        
    # Lancer la commande
    def run(self):
        if 'detectron2/projects/DensePose' in os.getcwd():
            print(os.getcwd())
        else:
            os.chdir('detectron2/projects/DensePose')
            print(os.getcwd())
        # subprocess.call(['python', 'apply_net.py', 'dump', 'configs/densepose_rcnn_R_50_FPN_DL_s1x.yaml', 'checkpoints/densepose_rcnn_R_50_FPN_DL_s1x.pkl', '/home/pc/Bureau/Test'], shell=True)
        os.system('python --version')
        print(torch.__version__, torch.version.cuda)
        os.system(self._cmd)
        os.chdir('../../..')
