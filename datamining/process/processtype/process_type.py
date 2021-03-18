from abc import ABC, abstractmethod

class ProcessType(ABC):

    @abstractmethod
    def process(self):
        pass