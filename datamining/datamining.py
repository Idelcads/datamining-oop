from .config.loader.config_loader import ConfigLoader
from .data.dataloader.flickr_loader import FlickrLoader
from .data.dataloader.local_loader import LocalLoader
from .process.process_service import ProcessServiceResizeCrop, ProcessServiceAlphaBox, ProcessServiceAPI, ProcessServiceAlphaPose


class DataminingResizeCrop():

    def __init__(self, configService: ConfigLoader):
        self._configService = configService
        cfg = self._configService.cfg
        # if cfg.DATALOADER.TYPE == "LOCAL": 
        self._dataLoader = LocalLoader(cfg.DATASET.NAME,
                                        cfg.RESIZE.PATH_PROCESS
                                        )
        self._processService = ProcessServiceResizeCrop(cfg) # TODO replace cfg by variable
    
    def run(self):
        images = self._dataLoader.load()
        
        self._processService.run(images)
        self._processService.save()

class DataminingAPI():

    def __init__(self, configService: ConfigLoader):
        self._configService = configService
        cfg = self._configService.cfg
        self._flickr = cfg.DATALOADER.TYPE
        if cfg.DATALOADER.TYPE == "FLICKR":
            self._dataLoader = FlickrLoader(cfg.DATALOADER.KEY, 
                                            cfg.DATALOADER.SECRET, 
                                            cfg.DATALOADER.KEYWORDS, 
                                            cfg.DATALOADER.COUNT,
                                            cfg.DATALOADER.MINSIZE,
                                            cfg.DATALOADER.MAXSIZE,
                                            cfg.DATALOADER.ORIGINAL_SIZE,
                                            cfg.DATASET.NAME,
                                            cfg.DATASET.RAW
                                            )
        self._processService = ProcessServiceAPI(cfg) # TODO replace cfg by variable

    def run(self):
        if self._flickr == "FLICKR":
            images = self._dataLoader.load()

class DataminingAlphaBox():

    def __init__(self, configService: ConfigLoader):
        self._configService = configService
        cfg = self._configService.cfg
        self.path = cfg.BBOX.PATH_PROCESS

        self._dataLoader = LocalLoader(cfg.DATASET.NAME,
                                        self.path
                                        )

        self._processService = ProcessServiceAlphaBox(cfg) # TODO replace cfg by variable

    
    def run(self):
        images = self._dataLoader.load()
        
        self._processService.run(images)
        self._processService.save()

class DataminingAlphaPose():

    def __init__(self, configService: ConfigLoader):
        self._configService = configService
        cfg = self._configService.cfg
        self.path = cfg.POSE_ESTIMATION.PATH_PROCESS

        self._dataLoader = LocalLoader(cfg.DATASET.NAME,
                                        self.path
                                        )

        self._processService = ProcessServiceAlphaPose(cfg) # TODO replace cfg by variable

    
    def run(self):
        images = self._dataLoader.load()
        
        self._processService.run(images)
        self._processService.save()
