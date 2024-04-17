from code_base.interfaces.ICalibrators import Calibrators
import math as math


class JrrnCalibrators(Calibrators):

    def __init__(self):
        Calibrators.__init__(self)

    def calibrate(self, r, vol, t):
        u = math.exp((r - vol * vol / 2) * t + vol * math.sqrt(t))
        d = math.exp((r - vol * vol / 2) * t - vol * math.sqrt(t))
        return (u, d, 1 / 2)
