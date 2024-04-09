import bisect, math

from code_base.interfaces.IVolatilities import Volatilities


class ImpliedVol(Volatilities):
    def __init__(self, ts, smiles):
        self.ts = ts
        self.smiles = smiles

    # linear interpolation in variance, along the strike line

    def Vol(self, t: float, k: float) -> float:
        # locate the interval t is in
        pos = bisect.bisect_left(self.ts, t)
        # if t is on or in front of first pillar,
        if pos == 0:
            return self.smiles[0].Vol(k)
        if pos >= len(self.ts) - 1:
            return self.smiles[-1].Vol(k)
        else:  # in between two brackets
            prevVol, prevT = self.smiles[pos - 1].Vol(k), self.ts[pos - 1]
            nextVol, nextT = self.smiles[pos].Vol(k), self.ts[pos]
            w = (nextT - t) / (nextT - prevT)
            prevVar = prevVol * prevVol * prevT
            nextVar = nextVol * nextVol * nextT
            return math.sqrt((w * prevVar + (1 - w) * nextVar) / t)

    def dVoldK(self, t: float, k: float) -> float:
        return (self.Vol(t, k + 0.001) - self.Vol(t, k - 0.001)) / 0.002

    def dVoldT(self, t: float, k: float) -> float:
        return (self.Vol(t + 0.005, k) - self.Vol(t, k)) / 0.005

    def dVol2dK2(self, t, k) -> float:
        return (self.Vol(t, k + 0.001) + self.Vol(t, k - 0.001) - 2 * self.Vol(t, k)) / 0.000001
