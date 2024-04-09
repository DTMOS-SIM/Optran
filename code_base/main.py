from infrastructure.options_typings import PayoffType

from services.options import (
    american_options as amer_opt,
    barrier_options as ko_opt,
    european_options as euro_opt,
    asian_options as asian_opt
)

from services.binomial_trees import binomial_tree_pricer

if __name__ == "__main__":


    amer_opts = amer_opt.AmericanOptions(1, 200, payoffType=PayoffType.Call)

    tree_pricing = binomial_tree_pricer.BinomialTreePricer()

    results = tree_pricing.generic_tree(S=100, r=0.01, vol=0.2, trade=amer_opts, n=2)

    print(results)
