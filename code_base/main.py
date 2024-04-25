from infrastructure.options_typings import PayoffType
from services.calibrators.model_calib.heston_model import HestonModel

from services.options import (
    american_options as amer_opt,
    barrier_options as bar_opt,
    european_options as euro_opt,
    asian_options as asian_opt,
    spread_options as spread_opt,
    tarf_options as tarf_opt
)

from code_base.services.pricers.binomial_tree_pricer import BinomialTreePricer

if __name__ == "__main__":
    S0 = 100  # initial asset price
    K = 100  # strike
    v0 = 0.1  # initial variance
    r = 0.03  # risk free rate
    kappa = 1.5768  # rate of mean reversion of variance process
    theta = 0.0398  # long-term mean variance
    sigma = 0.3  # volatility of volatility
    lamda = 0.575  # risk premium of variance
    rho = -0.5711  # correlation between variance and stock process
    tau = 1.  # time to maturity

    HestonModel = HestonModel(S0, K, v0, r, kappa, theta, sigma, lamda, rho, tau)
    result = HestonModel.price()
    print(result)
    '''
    |--------------------------------------------------------- Implement the main function ---------------------------------------------------------|
    amer_opt.AmericanOptions(2,140,PayoffType.Call)
    bar_opt.BarrierOption(95, 120, 0, 2, AmericanOptions(2,140,PayoffType.Call))
    euro_opt.EuropeanOption(2, 140, PayoffType.Call)
    asian_opt.AsianOption(2, 140, PayoffType.Call)
    spread_opt.SpreadOption(2, 140, PayoffType.Call)
    tarf_opt.Tarf(2, 140, PayoffType.Call)
    '''

    '''
    |--------------------------------------------------------- Dupire Volatility Simulation ---------------------------------------------------------|
    S, r, q = 1.25805, 0.01, 0.0
    iv = createTestImpliedVol(S, r, q, 1.0)
    plotTestImpliedVolSurface(iv)
    pdeCalibReport(S, r, q, iv)
    '''
