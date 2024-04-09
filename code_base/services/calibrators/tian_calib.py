from code_base.interfaces.ICalibrators import Calibrators
import math as math


class TianCalibrators(Calibrators):

    def __init__(self):
        super().__init__()

    def calibrate(self, r, vol, t):
        v = math.exp(vol * vol * t)
        u = 0.5 * math.exp(r * t) * v * (v + 1 + math.sqrt(v * v + 2 * v - 3))
        d = 0.5 * math.exp(r * t) * v * (v + 1 - math.sqrt(v * v + 2 * v - 3))
        p = (math.exp(r * t) - d) / (u - d)
        return (u, d, p)
