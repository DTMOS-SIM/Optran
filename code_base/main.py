from infrastructure.options_typings import PayoffType

from services.options import (
    american_options as amer_opt,
    barrier_options as bar_opt,
    european_options as euro_opt,
    asian_options as asian_opt,
    spread_options as spread_opt,
    tarf_options as tarf_opt
)

from services.binomial_trees import binomial_tree_pricer

if __name__ == "__main__":
    '''
    |--------------------------------------------------------- Implement the main function ---------------------------------------------------------|
    amer_opt.AmericanOptions(2,140,PayoffType.Call)
    bar_opt.BarrierOption(95, 120, 0, 2, AmericanOptions(2,140,PayoffType.Call))
    euro_opt.EuropeanOption(2, 140, PayoffType.Call)
    asian_opt.AsianOption(2, 140, PayoffType.Call)
    spread_opt.SpreadOption(2, 140, PayoffType.Call)
    tarf_opt.Tarf(2, 140, PayoffType.Call)
    '''
