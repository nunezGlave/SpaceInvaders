from abc import ABC, abstractmethod

class Scale(ABC):
    def __init__(self, type: int):
        self.scaleType = type

    @abstractmethod
    def newSize(self):
        pass

    @property
    def scaleNumber(self):
        return self.scaleType
