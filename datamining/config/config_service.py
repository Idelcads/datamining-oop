import ConfigLoader

class ConfigService():

    def __init__(loader : ConfigLoader = None ):
        if loader = None:
            self._loader = YamlLoader()
        else:
            self._loader = ConfigLoader()
    
    def load(config : str):
        self._loader.load()

    @property
    def cfg():
        return self._loader.cfg
