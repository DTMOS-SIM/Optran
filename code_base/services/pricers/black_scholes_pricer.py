import math
from code_base.infrastructure.options_typings import PayoffType
from code_base.simulators.vol_simulator import cnorm


# Black-Scholes analytic pricer
def black_scholes_pricer(S: float, r: float, q: float, vol: float, T: float, strike: float, payoffType: PayoffType):
    fwd = S * math.exp((r-q) * T)
    st_dev = vol * math.sqrt(T)
    d1 = math.log(fwd / strike) / st_dev + st_dev / 2
    d2 = d1 - st_dev
    if payoffType == PayoffType.Call:
        return math.exp(-r * T) * (fwd * cnorm(d1) - cnorm(d2) * strike)
    elif payoffType == PayoffType.Put:
        return math.exp(-r * T) * (strike * cnorm(-d2) - cnorm(-d1) * fwd)
    elif payoffType == PayoffType.BinaryCall:
        return math.exp(-r * T) * cnorm(d1)
    elif payoffType == PayoffType.BinaryPut:
        return math.exp(-r * T) * (1-cnorm(-d1))
    else:
        raise Exception("not supported payoff type", payoffType)