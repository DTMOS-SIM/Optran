import typing as t
from abc import ABC, abstractmethod


class Options(ABC):

    @abstractmethod
    def __init__(self, *_: t.Any, **__: t.Any) -> t.Any:
        self.expiry = None
        return

    @abstractmethod
    def value_at_node(self, *_: t.Any, **__: t.Any) -> t.Any:
        return

    @abstractmethod
    def payoff(self, *_: t.Any, **__: t.Any):
        return

    @abstractmethod
    def all_dates(self, *_: t.Any, **__: t.Any):
        return

    @abstractmethod
    def discounted_mc_payoff(self, *_: t.Any, **__: t.Any):
        return

    @abstractmethod
    def on_fixing_date(self, *_: t.Any, **__: t.Any):
        return

    @abstractmethod
    def asset_names(self, *_: t.Any, **__: t.Any):
        return
