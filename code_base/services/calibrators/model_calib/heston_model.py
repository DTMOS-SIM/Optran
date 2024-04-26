from typing import Callable

import numpy as np
# Parallel computation using numba
from numba import jit, njit, prange
from numba import cuda
from scipy.integrate import quad
from scipy.optimize import minimize


class HestonModel(object):
    """
    S0 = 100. # initial asset price
    K = 100. # strike
    v0 = 0.1 # initial variance
    r = 0.03 # risk free rate
    kappa = 1.5768 # rate of mean reversion of variance process
    theta = 0.0398 # long-term mean variance
    sigma = 0.3 # volatility of volatility
    lambd = 0.575 # risk premium of variance
    rho = -0.5711 # correlation between variance and stock process
    tau = 1. # time to maturity
    """

    def __init__(self,
                 spot: float,
                 strike: float,
                 interest: float,
                 maturity: float,
                 initial_variance: float = 0.0,
                 kappa: float = 0.0,
                 theta: float = 0.0,
                 sigma: float = 0.0,
                 rho: float = 0.0,
                 lamda: float = 0.0,
                 ) -> None:
        self._spot: [float] = spot
        self._strike: [float] = strike
        self._maturity: [float] = maturity
        self._interest: [float] = interest
        self._theta: float = theta
        self._kappa: float = kappa
        self._sigma: float = sigma
        self._rho: float = rho
        self._initial_variance: float = initial_variance
        self._lamda: float = lamda

          
    @staticmethod
    def define_heston_features(phi: float, kappa: float, theta: float, sigma: float, rho: float, lamda: float, maturity: float, interest: float, initial_variance: float, spot: float):
        # constants
        _a = kappa * theta
        _b = kappa + lamda

        # common terms w.r.t phi
        rspi = rho * sigma * phi * 1j

        # define d parameter given phi and b
        _d = np.sqrt(
            (rho * sigma * phi * 1j - _b) ** 2 + (phi * 1j + phi ** 2) * sigma ** 2)

        # define g parameter given phi, b and d
        g = (_b - rspi + _d) / (_b - rspi - _d)

        # calculate characteristic function by components

        exp1 = np.exp(interest * phi * 1j * maturity)
        term2 = spot ** (phi * 1j) * ((1 - g * np.exp(_d * maturity)) / (1 - g)) ** (
                -2 * _a / sigma ** 2)
        exp2 = np.exp(
            _a * maturity * (_b - rspi + _d) / sigma ** 2 + initial_variance * (_b - rspi + _d) * (
                    (1 - np.exp(_d * maturity)) / (1 - g * np.exp(_d * maturity))) / sigma ** 2)

        return exp1 * term2 * exp2

    @staticmethod
    def integrand(phi, interest, maturity, strike, kappa, theta, sigma, rho, lamda, initial_variance, spot):
        numerator = (np.exp(interest * maturity) *
                     HestonModel.define_heston_features(phi - 1j, kappa, theta, sigma, rho, lamda, maturity, interest, initial_variance, spot) - strike *
                     HestonModel.define_heston_features(phi, kappa, theta, sigma, rho, lamda, maturity, interest, initial_variance, spot))
        denominator = 1j * phi * strike ** (1j * phi)
        return numerator / denominator

    @staticmethod
    def price(spot, strike, interest, maturity, *args, **kwargs):
        real_integral, err = np.real(quad(HestonModel.integrand, 0, 100, args=args))
        return (spot - strike * np.exp(-interest * maturity)) / 2 + real_integral / np.pi

    def calibrate(self, squared_error, params):
        x0 = np.array([param["x0"] for key, param in params.items()])

        heston_bounds = [param["lbub"] for key, param in params.items()]

        result = minimize(squared_error, x0, tol=1e-3, method='SLSQP', options={'maxiter': 1e4}, bounds=heston_bounds)

        return result

    def squared_error(self, x: np.ndarray, x0: np.ndarray, last_trade_price: [float], rate: [float], strike: [float], maturity: [float], price: [float]):
        v0, kappa, theta, sigma, rho, lamda = [param for param in x]

        # Attempted to use scipy integrate quad module as constrained to single floats not arrays
        err = np.sum([
            (P_i - self.price(last_trade_price, K_i, v0, kappa, theta, sigma, rho, lamda, maturity, r_i)) ** 2 / len(price) for P_i, K_i, tau_i, r_i in zip(price, strike, maturity, rate)
        ])

        # Zero penalty term - no good guesses for parameters
        # pen = 0
        pen = np.sum([(x_i - x0_i) ** 2 for x_i, x0_i in zip(x, x0)])

        return err + pen
