from code_base.interfaces.ICalibrators import Calibrators
import math as math


class CrrCalibrators(Calibrators):

    def __init__(self):
        super().__init__()

    def calibrate(self, r, vol, t):
        b = math.exp(vol * vol * t + r * t) + math.exp(-r * t)
        u = (b + math.sqrt(b * b - 4)) / 2
        p = (math.exp(r * t) - (1 / u)) / (u - 1 / u)
        return (u, 1 / u, p)
