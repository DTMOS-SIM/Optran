import math
import numpy as np


class BlackScholesMC:
    def __init__(self, S0, vol, r, q):
        self.vol, self.S0, self.r, self.q = vol, S0, r, q

    @staticmethod
    def NumberOfFactors():
        return 1

    @staticmethod
    def GetTimeSteps(eventDates):
        # black scholes diffusion is exact, no need to add more dates
        return eventDates

    def Diffuse(self, dts, bs):
        xs = [math.log(self.S0)]
        dd = [0.0]
        for i in range(1, len(dts) + 1):
            a = (self.r - self.q - 0.5 * self.vol * self.vol) * dts[i - 1]
            b = self.vol * bs[0, i - 1] * math.sqrt(dts[i - 1])
            xs.append(xs[i - 1] + a + b)
            dd.append(dts[i - 1])
        return lambda t: math.exp(np.interp(t, dd, xs))


class LocalVolMC:
    def __init__(self, S0, T, lv, r, q):
        self.lv, self.S0, self.T, self.r, self.q = lv, S0, T, r, q

    @staticmethod
    def NumberOfFactors():
        return 1

    def GetTimeSteps(self, eventDates):
        nT = 100
        dt = self.T / nT
        for i in range(1, nT):
            eventDates.append(dt * i)
        return eventDates

    def Diffuse(self, dts, bs):
        xs = [math.log(self.S0)]
        dd = [0.0]
        for i in range(1, len(dts)):
            dt = dts[i] - dts[i - 1]
            vol = self.lv.LV(dts[i], math.exp(xs[i - 1]))
            a = (self.r - self.q - 0.5 * vol * vol) * dt
            b = vol * bs[0, i - 1] * math.sqrt(dt)
            xs.append(xs[i - 1] + a + b)
            dd.append(dt)
        return lambda t: math.exp(np.interp(t, dd, xs))


class DeterminsticIR:
    def __init__(self, r):
        self.r = r

    def NumberOfFactors(self):
        return 0

    def GetTimeSteps(self, eventDates):
        return eventDates

    def Diffuse(self, dts, bs):
        return lambda t: math.exp(-self.r * t)


def mcPricer(trade, models, corrMat, nPaths):
    assetNames = trade.assetNames()  # get all the assets involved for the payoff
    C = corrMat  # get correlation matrix from the market
    numFactors = C.shape[0]  # get total number of factors (brownians)
    L = np.linalg.cholesky(C)  # cholesky decomposition
    dts = []  # get simulation time steps
    for a in assetNames:
        dts += (models[a].GetTimeSteps(trade.AllDates()))
    dts = np.unique(dts)
    dts = np.sort(dts)

    sum, hsquare, nT = 0, 0, len(dts)
    for i in range(nPaths):
        # generate independent bronian increments,
        brownians = np.zeros((numFactors, nT))
        for j in range(numFactors):
            brownians[j] = np.random.normal(0, 1, nT)
        brownians = np.matmul(L, brownians)  # correlate them using L
        bidx, fobs = 0, dict()  # fobs is a dict from asset name to observable,
        # each observable if a function from t to the observation price
        for k in assetNames:
            # pass the brownians to the model to generate the observation functions
            model = models[k]
            nF = model.NumberOfFactors()
            bs = brownians[bidx:bidx + nF, :]  # (bidx:bidx + nF, :]
            fobs[k] = model.Diffuse(dts, bs)
            bidx += nF
        # call the payoff function to obtain the discounted cashflows
        h = trade.DiscountedMCPayoff(fobs)
        sum += h
        hsquare += h * h
    pv = sum / nPaths
    se = math.sqrt((hsquare / nPaths - pv * pv) / nPaths)
    return pv, se