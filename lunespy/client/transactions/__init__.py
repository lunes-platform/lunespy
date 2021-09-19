from abc import ABCMeta, abstractmethod

class BaseTransaction(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def ready(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def transaction(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def send(self) -> dict:
        raise NotImplementedError