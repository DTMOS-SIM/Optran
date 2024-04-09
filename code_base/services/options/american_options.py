from code_base.interfaces.IOptions import Options
from code_base.infrastructure.options_typings import PayoffType


class AmericanOptions(Options):

    def __init__(self, expiry, strike, payoffType):
        self.expiry = expiry
        self.strike = strike
        self.payoffType = payoffType

    def all_dates(self):
        pass

    def discounted_mc_payoff(self, fobs):
        pass

    def on_fixing_date(self, t):
        pass

    def asset_names(self):
        pass

    def payoff(self, S):
        if self.payoffType == PayoffType.Call:
            return max(S - self.strike, 0)
        elif self.payoffType == PayoffType.Put:
            return max(self.strike - S, 0)
        else:
            raise Exception("payoffType not supported: ", self.payoffType)

    def value_at_node(self, t, S, continuation):
        return max(self.payoff(S), continuation)
