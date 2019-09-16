from abc import ABCMeta, abstractmethod

class Factory(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load():
        pass