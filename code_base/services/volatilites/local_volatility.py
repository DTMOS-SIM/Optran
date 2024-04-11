import math
from code_base.interfaces.IVolatilities import Volatilities
from implied_volatility import ImpliedVol
from flat_volatility import FlatVol


class LocalVolatilities(Volatilities):
    def __init__(self, iv: FlatVol | ImpliedVol, S0: float, rd: float, rf: float) -> None:
        self.iv = iv
        self.S0 = S0
        self.rd = rd
        self.rf = rf

    def Vol(self, t: float, s: float) -> float:
        if t < 1e-6:
            return self.iv.Vol(t, s)
        imp = self.iv.Vol(t, s)
        # first derivative with respect to strike price
        dv_dk = self.iv.dVold_K(t, s)
        # First derivative with respect to time
        dv_dt = self.iv.dVold_T(t, s)
        # Second derivatives with respect to strike price
        d2v_dk2 = self.iv.dVol2_dK2(t, s)
        d1 = (math.log(self.S0 / s) + (self.rd - self.rf) * t + imp * imp * t / 2) / imp / math.sqrt(t)
        numerator = imp * imp + 2 * t * imp * dv_dk + 2 * (self.rd - self.rf) * s * t * imp * dv_dk
        denominator = (1 + s * d1 * math.sqrt(t) * dv_dt) ** 2 + s * s * t * imp * (
                d2v_dk2 - d1 * math.sqrt(t) * dv_dk * dv_dk)
        local_var = min(max(numerator / denominator, 1e-8), 1.0)
        if numerator < 0:  # floor local volatility
            local_var = 1e-8
        if denominator < 0:  # cap local volatility
            local_var = 1.0
        return math.sqrt(local_var)
