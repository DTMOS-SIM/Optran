import typing as t

from code_base.interfaces.IOptions import Options


class KnockOutOption(Options):

    def __init__(self, downBarrier, upBarrier, barrierStart, barrierEnd, underlyingOption):
        self.underlyingOption = underlyingOption
        self.barrierStart = barrierStart
        self.barrierEnd = barrierEnd
        self.downBarrier = downBarrier
        self.upBarrier = upBarrier
        self.expiry = underlyingOption.expiry

    def payoff(self, S):
        return self.underlyingOption.payoff(S)

    def value_at_node(self, t, S, continuation):
        if self.barrierStart < t < self.barrierEnd:
            if self.upBarrier is not None and S > self.upBarrier:
                return 0
            elif self.downBarrier is not None and S < self.downBarrier:
                return 0
        return continuation

    def all_dates(self, *_: t.Any, **__: t.Any):
        pass

    def discounted_mc_payoff(self, *_: t.Any, **__: t.Any):
        pass

    def on_fixing_date(self, *_: t.Any, **__: t.Any):
        pass

    def asset_names(self, *_: t.Any, **__: t.Any):
        pass