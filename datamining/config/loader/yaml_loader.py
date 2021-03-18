from .config import get_cfg_defaults
from .config_loader import ConfigLoader

class YamlLoader(ConfigLoader):
    def __init__(self, config : str):
        self._cfg = get_cfg_defaults()
        self._cfg.merge_from_file(config)
        self._cfg.freeze()
        
    def load(self, config : str):
        pass
        

    @property
    def cfg(self):
        return self._cfg