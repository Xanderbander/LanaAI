import backtrader as bt
from .indicators import EMACrossOver, RSISignal

class MyStrategy(bt.Strategy):
    params = (
        ('ema1_period', 20),
        ('ema2_period', 50),
        ('rsi_period', 14),
        ('rsi_upper', 70),
        ('rsi_lower', 30),
    )

    def __init__(self):
        self.ema1 = EMACrossOver(self.data.close, period=self.params.ema1_period)
        self.ema2 = EMACrossOver(self.data.close, period=self.params.ema2_period)
        self.rsi = RSISignal(self.data.close, period=self.params.rsi_period,
                             upper=self.params.rsi_upper, lower=self.params.rsi_lower)

    def next(self):
        if self.ema1.crossover > 0 and self.rsi.signal > 0:
            self.buy()
        elif self.ema2.crossover < 0 and self.rsi.signal < 0:
            self.sell()

