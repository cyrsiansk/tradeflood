from linktester import classes
from turn_system import turn, turn_execution
from typing import TypeVar

F = TypeVar("F", bound=classes.HistoryFetcher)


class BinanceHistoryFetcher(classes.HistoryFetcher):
    pass


class Candle:
    t: int
    value: float

    def __init__(self, t, value):
        self.t = t
        self.value = value

    def __repr__(self):
        return f"Candle({self.t}, {self.value})"


class HistoryFetcherCandleInterface:
    history_fetcher: F

    def get_data(self, start, amount, ticker):
        pass


@classses.link(BinanceHistoryFetcher, Candle)
class BinanceHistoryFetcherCandleInterface(HistoryFetcherCandleInterface):
    @turn_execution
    def process_data(self, data, start):
        data = data()
        result = []
        for c in data:
            result.append(Candle(start, c))
            start += 1
        return result

    @turn
    def get_data(self, start, amount, ticker):
        data = self.history_fetcher.get_data(start, amount, ticker)
        return self.process_data(data, start)

