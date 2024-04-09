import typing as t
from code_base.interfaces.IOptions import Options
from code_base.infrastructure.options_typings import PayoffType


class Tarf(Options):

    def __init__(self, assetName, fixings, payoffFun, targetGain):
        self.fixings = fixings
        self.payoffFun = payoffFun
        self.assetName = assetName
        self.targetGain = targetGain

    def all_dates(self):
        return self.fixings

    def discounted_mc_payoff(self, fobs):
        df = fobs["DF.USD"](self.fixings[-1])
        accum, discounted_po = 0, 0
        for t in self.fixings:
            df = fobs["DF.USD"](t)
            po = self.payoffFun(fobs[self.assetName](t))
            accum += po
            discounted_po += df * po
            if accum > self.targetGain:
                break  # triggers knockout
        return discounted_po

    def asset_names(self):
        return [self.assetName, "DF.USD"]

    '''
    |--------------------------------------------------------------------Optional Parameters--------------------------------------------------------------------|
    '''

    def value_at_node(self, *_: t.Any, **__: t.Any) -> t.Any:
        pass

    def payoff(self, *_: t.Any, **__: t.Any):
        pass

    def on_fixing_date(self, *_: t.Any, **__: t.Any):
        pass
