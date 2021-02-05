from abc import ABC

class BaseModule(ABC):
    def __init__(self):
        pass

    @property
    def conversation(self):
        pass

    @abstractmethod
    def __call__(self):
        pass

