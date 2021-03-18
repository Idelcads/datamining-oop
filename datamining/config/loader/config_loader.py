from abc import ABC, abstractmethod

class ConfigLoader(ABC):

    @abstractmethod
    def load(self, config : str):
        pass

    @abstractmethod
    def cfg(self):
        pass