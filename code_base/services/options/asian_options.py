import typing as t
import numpy as np
from code_base.interfaces.IOptions import Options


class AsianOption(Options):

    def __init__(self, assetName, asset, fixings, payoffFun, As, nT):
        self.assetName = assetName
        self.fixings = fixings
        self.payoffFun = payoffFun
        self.expiry = fixings[-1]
        self.nFix = len(fixings)
        self.As, self.nT, self.dt = As, nT, self.expiry / nT
        self.asset = asset

    def payoff(self, *_: t.Any, **__: t.Any):
        pass

    def all_dates(self):
        return self.fixings

    def discounted_mc_payoff(self, fobs):
        df = fobs["DF.USD"](self.fixings[-1])
        avg = 0
        for t in self.fixings:
            avg += fobs[self.assetName](t)
        return df * self.payoffFun(avg / self.nFix)

    def asset_names(self):
        return [self.assetName, "DF.USD"]

    def on_fixing_date(self, t):
        # we say t is on a fixing date if there is a fixing date in (t-dt, t]
        return filter(lambda x: t - self.dt < x <= t, self.fixings)

    def value_at_node(self, t, S, continuation):
        if continuation is None:
            return [self.payoffFun((a * float(self.nFix - 1) + S) / self.nFix) for a in self.As]
        else:
            node_values = continuation
            if self.on_fixing_date(t):
                i = len(list(filter(lambda x: x < t, self.fixings)))  # number of previous fixings
                if i > 0:
                    a_hats = [(a * (i - 1) + S) / i for a in self.As]
                    node_values = [np.interp(a, self.As, continuation) for a in a_hats]
        return node_values
