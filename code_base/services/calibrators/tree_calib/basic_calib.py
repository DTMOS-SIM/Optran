from code_base.interfaces.ICalibrators import Calibrators
import math as math


class BasicCalibrators(Calibrators):

    def __init__(self):
        super().__init__()

    def calibrate(r, vol, t):
        u = math.exp(vol * math.sqrt(t))
        p = (math.exp(r * t) - (1 / u)) / (u - 1 / u)
        return (u, 1 / u, p)
