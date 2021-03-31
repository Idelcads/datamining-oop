import os

class AlphaPoseMapper():
    def __init__(self, config, path, case):
        self._case = case

        if self._case == 0: # Cas BBOX
            self._inputpath = os.path.join(os.getcwd(),'datasets', config.DATASET.NAME, path)
            self._vispred = config.BBOX.VIS_PRED
            self._tresh = config.BBOX.TRESH
            self._model = config.BBOX.MODEL
            self._outputpath = os.path.join(os.getcwd(),'datasets', config.DATASET.NAME, 'temp/bbox')
        
        elif self._case == 1: # Cas POSE_ESTIMATION
            self._inputpath = os.path.join(os.getcwd(),'datasets', config.DATASET.NAME, path)
            self._vispred = config.POSE_ESTIMATION.VIS_PRED
            self._tresh = config.POSE_ESTIMATION.TRESH
            self._model = config.POSE_ESTIMATION.MODEL
            self._outputpath = os.path.join(os.getcwd(),'datasets', config.DATASET.NAME, 'temp/pose')

        os.makedirs(self._outputpath, exist_ok=True)
        self._cfg, self._chekpoint = AlphaPoseMapper.check_model(self._model)
        self._cmd = 'python3 scripts/demo_inference.py --indir ' + self._inputpath + ' --outdir ' + self._outputpath\
               + ' --cfg ' + self._cfg + ' --checkpoint ' + self._chekpoint 

        if self._vispred == 'yes':
            self._cmd = self._cmd + ' --save_img'
        if self._case == 0:
            self._cmd = self._cmd + ' --showbox '
        
    # Lancer la commande
    def run(self):
        if 'AlphaPose' in os.getcwd():
            print(os.getcwd())
        else:
            os.chdir('AlphaPose')
            print(os.getcwd())
        os.system(self._cmd)
        os.chdir('..')
    
    def check_model(val):
        if val == 17:
            cfg = 'configs/coco/resnet/256x192_res152_lr1e-3_1x-duc.yaml'
            checkpoint = 'pretrained_models/fast_421_res152_256x192.pth'
        elif val == 26:
            cfg = 'configs/halpe_26/resnet/256x192_res50_lr1e-3_1x.yaml'
            checkpoint = 'pretrained_models/halpe26_fast_res50_256x192.pth'
        elif val == 136:
            cfg = 'configs/halpe_136/resnet/256x192_res50_lr1e-3_2x-regression.yaml'
            checkpoint = 'pretrained_models/halpe136_fast_res50_256x192.pth'
        return cfg, checkpoint
