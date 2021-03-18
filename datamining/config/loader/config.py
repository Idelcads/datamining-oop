from yacs.config import CfgNode as CN

_C = CN()

_C.DATASET = CN()
_C.DATASET.NAME = ''
_C.DATASET.ANNOTATIONS = 'annotations'
_C.DATASET.RAW = 'raw'
_C.DATASET.TEST_IMG = 'test_img'
_C.DATASET.TEST_LABEL = 'test_label'
_C.DATASET.TRAIN_IMG = 'train_img'
_C.DATASET.TRAIN_LABEL = 'train_label'
_C.DATASET.VAL_IMG = 'val_img'
_C.DATASET.VAL_LABEL = 'val_label'

_C.DATALOADER = CN()
_C.DATALOADER.TYPE = 'FOLDER' # TODO change to CN 
_C.DATALOADER.KEY = ''
_C.DATALOADER.SECRET = ''
_C.DATALOADER.KEYWORDS = []
_C.DATALOADER.COUNT = 10
_C.DATALOADER.MINSIZE = 720
_C.DATALOADER.MAXSIZE = 1024
_C.DATALOADER.ORIGINAL_SIZE = 'no'

_C.PROCESS = CN()
_C.PROCESS.RESIZE = 'no'
_C.PROCESS.BBOX = 'no'
_C.PROCESS.POSE_ESTIMATION = 'no'
_C.PROCESS.ORDER = ["loader","bbox","pose_estimation","resize"]
# _C.PROCESS.CROP = 0

_C.RESIZE = CN()
_C.RESIZE.SIZE = '500x500'
_C.RESIZE.INTERPOLATION = 2
_C.RESIZE.PATH_PROCESS = "raw"

_C.BBOX = CN()
_C.BBOX.VIS_PRED = "no"
_C.BBOX.TRESH = 0.8
_C.BBOX.MIN_SIZE = 30
_C.BBOX.PATH_PROCESS = "raw"
_C.BBOX.ONLY_ONE = 'no'
_C.BBOX.SAVE_PRED = 'no'
_C.BBOX.MODEL = 17

_C.POSE_ESTIMATION = CN()
_C.POSE_ESTIMATION.VIS_PRED = 'no'
_C.POSE_ESTIMATION.SAVE_PRED = 'no'
_C.POSE_ESTIMATION.TRESH = 0.8
_C.POSE_ESTIMATION.PATH_PROCESS = "raw"
_C.POSE_ESTIMATION.ONLY_ONE = "no"
_C.POSE_ESTIMATION.SAVE_RGB = "yes"
_C.POSE_ESTIMATION.SAVE_BLACK = "no"
_C.POSE_ESTIMATION.SAVE_OTHER = "no"
_C.POSE_ESTIMATION.PATH_OTHER = ""
_C.POSE_ESTIMATION.DRAW_THICKNESS_LINES = 1
_C.POSE_ESTIMATION.DRAW_THICKNESS_POINTS = 1
_C.POSE_ESTIMATION.MODEL = 17

def get_cfg_defaults():
  """Get a yacs CfgNode object with default values for my_project."""
  # Return a clone so that the defaults will not be altered
  # This is for the "local variable" use pattern
  return _C.clone()

# Alternatively, provide a way to import the defaults as
# a global singleton:
# cfg = _C  # users can `from config import cfg`