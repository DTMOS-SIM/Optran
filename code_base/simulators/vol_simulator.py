import math
from scipy import optimize
from code_base.infrastructure.options_typings import PayoffType
from code_base.services.volatilites.cublic_spline import SmileCubicSpline


def cnorm(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def fwd_delta(fwd, stdev, strike, payoffType):
    d1 = math.log(fwd / strike) / stdev + stdev / 2
    if payoffType == PayoffType.Call:
        return cnorm(d1)
    elif payoffType == PayoffType.Put:
        return - cnorm(-d1)
    else:
        raise Exception("not supported payoff type", payoffType)


def strike_from_delta(S, r, q, T, vol, delta, payoffType):
    fwd = S * math.exp((r - q) * T)
    if payoffType == PayoffType.Put:
        delta = -delta
    f = lambda K: (fwd_delta(fwd, vol * math.sqrt(T), K, payoffType) - delta)
    a, b = 0.0001, 10000
    return optimize.brentq(f, a, b)


def smile_from_marks(T, S, r, q, atmvol, bf25, rr25, bf10, rr10):
    c25 = bf25 + atmvol + rr25 / 2
    p25 = bf25 + atmvol - rr25 / 2
    c10 = bf10 + atmvol + rr10 / 2
    p10 = bf10 + atmvol - rr10 / 2

    ks = [strike_from_delta(S, r, q, T, p10, 0.1, PayoffType.Put),
          strike_from_delta(S, r, q, T, p25, 0.25, PayoffType.Put),
          S * math.exp((r - q) * T),
          strike_from_delta(S, r, q, T, c25, 0.25, PayoffType.Call),
          strike_from_delta(S, r, q, T, c10, 0.1, PayoffType.Call)]
    # print(T, ks)
    return SmileCubicSpline(ks, [p10, p25, atmvol, c25, c10])
