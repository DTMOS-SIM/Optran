import math

from code_base.interfaces.ICalibrators import Calibrators
from code_base.interfaces.IOptions import Options
from code_base.interfaces.ITreePricer import TreePricer


class BinomialTreePricer(TreePricer):

    def __init__(S: float, r: float, vol: float, trade: Options, n: int) -> None:

        pass

    def generic_tree(S: float, r: float, vol: float, trade: Options, n: int):
        t = trade.expiry / n
        b = math.exp(vol * vol * t + r * t) + math.exp(-r * t)
        u = (b + math.sqrt(b * b - 4)) / 2
        p = (math.exp(r * t) - (1 / u)) / (u - 1 / u)
        # d = 1 / u

        # set up the last time slice, there are n+1 nodes at the last time slice
        vs = [trade.payoff(S * u ** (n - i - i)) for i in range(n + 1)]

        # iterate backward
        for i in range(n - 1, -1, -1):

            # calculate the value of each node at time slide i, there are i nodes
            for j in range(i + 1):
                node_stock = S * u ** (i - j - j)
                continuation = math.exp(-r * t) * (vs[j] * p + vs[j + 1] * (1 - p))
                vs[j] = trade.value_at_node(t * i, node_stock, continuation)

        return vs[0]

    @staticmethod
    def binomial_pricer(S: float, r: float, vol: float, trade: Options, n: int, calib: Calibrators):
        t = trade.expiry / n
        (u, d, p) = calib.calibrate(r, vol, t)
        # set up the last time slice, there are n+1 nodes at the last time slice
        vs = [trade.payoff(S * u ** (n - i) * d ** i) for i in range(n + 1)]
        # iterate backward
        for i in range(n - 1, -1, -1):
            # calculate the value of each node at time slide i, there are i nodes
            for j in range(i + 1):
                node_S = S * u ** (i - j) * d ** j
                continuation = math.exp(-r * t) * (vs[j] * p + vs[j + 1] * (1 - p))
                vs[j] = trade.value_at_node(t * i, node_S, continuation)
        return vs[0]
