from abc import ABCMeta, abstractmethod

class Factory(metaclass=ABCMeta):
    """
    Abstract class that defines a person operations
    and common attributes.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load():
        """
        Abstract method that loads the class depending on the factory.
        """
        pass