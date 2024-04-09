import typing as t
from abc import ABC, abstractmethod


class Calibrators(ABC):

    @abstractmethod
    def __init__(self, *_: t.Any, **__: t.Any) -> t.Any:
        return

    @abstractmethod
    def calibrate(self, *_: t.Any, **__: t.Any) -> t.Any:
        return
