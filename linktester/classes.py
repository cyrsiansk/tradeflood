from turn_system import *
import numpy as np


class HistoryFetcher:
    @turn_execution
    def get_data(self, start, amount, ticker):
        seed = start
        for c in ticker:
            seed += ord(c)*1000

        np.random.seed(seed)
        return np.random.rand(amount)


class HistoryFetcherCandleInterface:
    history_fetcher: F

    @turn
    def get_data(self, start, amount, ticker):
        pass
