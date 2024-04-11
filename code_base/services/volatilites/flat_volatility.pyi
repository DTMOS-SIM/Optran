from code_base.interfaces.IVolatilities import Volatilities

class FlatVol(Volatilities):
    def __init__(self, vol: float) -> float:
        self.vol = vol

    def Vol(self, t: float, k: float) -> float:
        return self.vol

    @staticmethod
    def dVold_K(t: float, k: float) -> int:
        return 0

    @staticmethod
    def dVold_T(self, t: float, k: float) -> int:
        return 0

    @staticmethod
    def dVol2_dK2(self, t: float, k: float) -> int:
        return 0