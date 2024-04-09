import typing as t
from abc import ABC, abstractmethod


class TreePricer(ABC):

    @abstractmethod
    def __init__(self, *_: t.Any, **__: t.Any) -> None:
        pass

    def pricing(self):
        pass