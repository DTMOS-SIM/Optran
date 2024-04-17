import math
import typing as t

from code_base.interfaces.ICalibrators import Calibrators


class TreeCalib(Calibrators):

    def __init__(self, r, q1, q2, vol1, vol2, rho, T) -> None:
        self.r = r
        self.q1 = q1
        self.q2 = q2
        self.vol1 = vol1
        self.vol2 = vol2
        self.rho = rho
        self.T = T
        pass

    def calibrate(self) -> t.Tuple[float, float, float, float, float, float]:
        sqrt = math.sqrt(self.T)
        v1 = self.r - self.q1 - self.vol1 * self.vol1 / 2
        v2 = self.r - self.q2 - self.vol2 * self.vol2 / 2
        x1 = self.vol1 * sqrt
        x2 = self.vol2 * sqrt
        a = x1 * x2
        b = x2 * v1 * self.T
        c = x1 * v2 * self.T
        d = self.rho * self.vol1 * self.vol2 * t
        puu = (a + b + c + d) / 4 / a
        pud = (a + b - c - d) / 4 / a
        pdu = (a - b + c - d) / 4 / a
        pdd = (a - b - c + d) / 4 / a
        return x1, x2, puu, pud, pdu, pdd