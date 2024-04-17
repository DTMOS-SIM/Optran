from code_base.interfaces.ICalibrators import Calibrators
import math as math


class JreqCalibrators(Calibrators):

    def __init__(self):
        super().__init__()

    def calibrate(self, r, vol, t):
        u = math.exp((r - vol * vol / 2) * t + vol * math.sqrt(t))
        d = math.exp((r - vol * vol / 2) * t - vol * math.sqrt(t))
        p = (math.exp(r * t) - d) / (u - d)
        return (u, d, p)
