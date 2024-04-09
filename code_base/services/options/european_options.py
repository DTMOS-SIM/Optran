import typing as t

from code_base.interfaces.IOptions import Options
from code_base.infrastructure.options_typings import PayoffType


class EuropeanOption(Options):

    def __init__(self, assetName, expiry, strike, payoffType):
        self.assetName = assetName
        self.expiry = expiry
        self.strike = strike
        self.payoffType = payoffType

    def payoff(self, S):
        if self.payoffType == PayoffType.Call:
            return max(S - self.strike, 0)
        elif self.payoffType == PayoffType.Put:
            return max(self.strike - S, 0)
        elif self.payoffType == PayoffType.BinaryCall:
            if S > self.strike:
                return 1.0
            else:
                return 0.0
        elif self.payoffType == PayoffType.BinaryPut:
            if S < self.strike:
                return 1.0
            else:
                return 0.0
        else:
            raise Exception("payoffType not supported: ", self.payoffType)

    def value_at_node(self, t, S, continuation):
        if continuation is None:
            return self.payoff(S)
        else:
            return continuation

    def asset_names(self):
        return [self.assetName, "DF.USD"]

    def all_dates(self):
        return [self.expiry]

    def discounted_mc_payoff(self, fobs):
        df = fobs["DF.USD"](self.expiry)
        po = self.payoff(fobs[self.assetName](self.expiry))
        return po * df
