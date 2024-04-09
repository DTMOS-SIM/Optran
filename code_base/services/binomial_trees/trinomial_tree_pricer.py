import math
from code_base.interfaces.ITreePricer import TreePricer


class TrinomialTreePricer(TreePricer):

    def __init__(self, S, r, q, vol, trade, n, lamda):
        self.S = S
        self.r = r
        self.q = q
        self.vol = vol
        self.trade = trade
        self.n = n
        self.lamda = lamda

    def pricing(self):
        t = self.trade.expiry / self.n
        u = math.exp(self.lamda * self.vol * math.sqrt(t))
        mu = self.r - self.q
        pu = 1 / 2 / self.lamda / self.lamda + (mu - self.vol * self.vol / 2) / 2 / self.lamda / self.vol * math.sqrt(t)
        pd = 1 / 2 / self.lamda / self.lamda - (mu - self.vol * self.vol / 2) / 2 / self.lamda / self.vol * math.sqrt(t)
        pm = 1 - pu - pd
        # set up the last time slice, there are 2n+1 nodes at the last time slice
        # counting from the top, the i-th node's stock price is S * u^(n - i), i from 0 to n+1
        vs = [self.trade.payoff(self.S * u ** (self.n - i)) for i in range(2 * self.n + 1)]
        # iterate backward
        for i in range(self.n - 1, -1, -1):
            # calculate the value of each node at time slide i, there are i nodes
            for j in range(2*i + 1):
                node_S = self.S * u ** (i - j)
                continuation = math.exp(-self.r * t) * (vs[j] * pu + vs[j+1] * pm + vs[j+2] * pd)
                vs[j] = self.trade.valueAtNode(t * i, node_S, continuation)
        return vs[0]