import typing as t
from abc import ABC, abstractmethod


class Volatilities(ABC):

    @abstractmethod
    def __init__(self, *_: t.Any, **__: t.Any) -> None:
        pass
        
    @abstractmethod
    def Vol(self):
        pass
