from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt


# Define custom indicators
class EMA(bt.Indicator):
    lines = ('ema',)

    params = (('period', 20),)

    def __init__(self):
        self.lines.ema = bt.indicators.ExponentialMovingAverage(self.data, period=self.params.period)


class RSI(bt.Indicator):
    lines = ('rsi',)
    
    params = (('period', 14),)
    
    def __init__(self):
        self.lines.rsi = bt.indicators.RSI(self.data, period=self.params.period)


class MACD(bt.Indicator):
    lines = ('macd', 'signal', 'histogram')

    params = (
        ('period_me1', 12),
        ('period_me2', 26),
        ('period_signal', 9),
    )

    def __init__(self):
        me1 = bt.indicators.ExponentialMovingAverage(self.data, period=self.params.period_me1)
        me2 = bt.indicators.ExponentialMovingAverage(self.data, period=self.params.period_me2)

        self.lines.macd = me1 - me2
        self.lines.signal = bt.indicators.ExponentialMovingAverage(self.lines.macd, period=self.params.period_signal)
        self.lines.histogram = self.lines.macd - self.lines.signal
