import math
import numpy as np


class SABRModel(object):

    def __init__(self, forward_rate: float, strike_price: float, start_date_count: float, alpha: float, rho: float,
                 nu: float, beta: float):
        self.forward_rate = forward_rate
        self.strike_price = strike_price
        self.start_date_count = start_date_count
        self.alpha = alpha
        self.rho = rho
        self.nu = nu
        self.beta = beta

    @staticmethod
    def calibrate_model(self, F, strikes, T, market_vol, x, beta):
        err = 0.0
        for vol, K in zip(market_vol, strikes):
            err += (vol - self.compute_sigma(F, K, T, x[0], x[1], x[2], beta)) ** 2
        return err

    @staticmethod
    def compute_sigma(self):
        X = self.strike_price

        # ATM Volatility Formula
        # For options where the forward rate F is equal to the strike price K, this particular algorithm adjusts the basic
        # SABR formula to account for the time to maturity T and includes corrections for skewness and kurtosis through
        # the parameters α, ρ, ν, and β
        if abs(self.forward_rate - self.strike_price) < 1e-12:
            numer1 = (((1 - self.beta) ** 2) / 24) * self.alpha * self.alpha / (
                    self.forward_rate ** (2 - 2 * self.beta))
            numer2 = 0.25 * self.rho * self.beta * self.nu * self.alpha / (self.forward_rate ** (1 - self.beta))
            numer3 = ((2 - 3 * self.rho * self.rho) / 24) * self.nu * self.nu
            VolAtm = self.alpha * (1 + (numer1 + numer2 + numer3) * self.start_date_count) / (
                        self.forward_rate ** (1 - self.beta))
            sabr_sigma = VolAtm

        # Non ATM Volatility Formula
        # For options where the forward rate F is not equal to the strike price K, it involves a more complex calculation
        # that adjusts for the relative position of the forward rate to the strike, incorporating a scaling factor based
        # on z and ζ that adjusts for the actual difference between the forward and strike prices.
        else:
            # Scaling factor for non atm vol formula
            z = (self.nu / self.alpha) * ((self.forward_rate * X) ** (0.5 * (1 - self.beta))) * np.log(
                self.forward_rate / X)
            # Scaling factor for non atm vol formula
            zhi = np.log((((1 - 2 * self.rho * z + z * z) ** 0.5) + z - self.rho) / (1 - self.rho))

            # First 2 multiplicative terms of the SABR formula indicates:
            # Long-Term Variance Adjustment, accounts for the long-term variance skew in the model,
            # adjusting the base volatility based on β and the ratio of forward to strike price.
            numer1 = (((1 - self.beta) ** 2) / 24) * (
                        (self.alpha * self.alpha) / ((self.forward_rate * X) ** (1 - self.beta)))

            # Second term of the SABR formula indicates:
            # Correlation Adjustment, corrects for the correlation (ρ) between the asset price and its volatility,
            # multiplied by the beta factor and the vol-of-vol (ν), and α
            numer2 = 0.25 * self.rho * self.beta * self.nu * self.alpha / (
                    (self.forward_rate * X) ** ((1 - self.beta) / 2))

            # Third term of the SABR formula indicates:
            # Volatility Skewness Adjustment, reflects the skewness in the volatility surface,
            # adjusted for the vol-of-vol (ν) and the correlation parameter (ρ)
            numer3 = ((2 - 3 * self.rho * self.rho) / 24) * self.nu * self.nu

            # Final SABR model for atm volatility adjustments
            numer = self.alpha * (1 + (numer1 + numer2 + numer3) * self.start_date_count) * z

            # These terms are part of the Hagan et al. (2002) approximation for the SABR model's implied volatility

            # denom1: This term comes from the expansion of the Black-Scholes implied volatility formula to account for
            # the convexity of the volatility smile around the ATM point. It is the second-order term in the Taylor
            # series expansion around the ATM volatility. Accounts for the impact of the difference between the forward rate
            # F and the strike K
            denom1 = ((1 - self.beta) ** 2 / 24) * (np.log(self.forward_rate / X)) ** 2

            # denom2: Further refines the adjustment for the curvature of the volatility smile. It is a fourth-order
            # term that becomes significant when the difference between the forward rate and the strike price is large,
            # or when the volatility of volatility (the nu parameter) is high
            denom2 = (((1 - self.beta) ** 4) / 1920) * ((np.log(self.forward_rate / X)) ** 4)

            denom = ((self.forward_rate * X) ** ((1 - self.beta) / 2)) * (1 + denom1 + denom2) * zhi

            sabr_sigma = numer / denom

        return sabr_sigma



    '''
    |-------------------------------------
    start = date_count_df.Start
    tenor = date_count_df.Tenor
    
    alpha_results = []
    rho_results = []
    nu_results = []
    
    initial_guess = [0.1,-0.1,0.1]
    
    for i in range(len(pvbp)):
        results = least_squares(lambda x: sabr_calibration(libor_forward_rate[i], strike[i], int(start[i]), swaption_data.values[i][2:], x, 0.9), initial_guess, bounds = ([0.0,-1.0,0.0], [np.inf, 1, np.inf]))
    
        alpha_results.append(results.x[0])
        rho_results.append(results.x[1])
        nu_results.append(results.x[2])
    '''