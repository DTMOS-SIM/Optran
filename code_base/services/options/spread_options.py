import typing as t

from code_base.interfaces.IOptions import Options


class SpreadOption(Options):

    def __init__(self, asset1, asset2, expiry):
        self.expiry = expiry
        self.asset1, self.asset2 = asset1, asset2

    def payoff(self, S1, S2):
        return max(S1 - S2, 0)

    def value_at_node(self, t, S1, S2, continuation):
        return continuation

    def asset_names(self):
        return [self.asset1, self.asset2, "DF.USD"]

    def all_dates(self):
        return [self.expiry]

    def discounted_mc_payoff(self, fobs):
        df = fobs["DF.USD"](self.expiry)
        s1 = fobs[self.asset1](self.expiry)
        s2 = fobs[self.asset2](self.expiry)
        return df * max(s1 - s2, 0)

    ''' 
    |--------------------------------------------------------------------Optional Parameters--------------------------------------------------------------------|
    '''

    def on_fixing_date(self, *_: t.Any, **__: t.Any):
        pass
