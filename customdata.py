import backtrader as bt
import pandas as pd

class CustomData(bt.feeds.GenericCSVData):
    params = (
        ('nullvalue', 0.0),
        ('dtformat', '%Y-%m-%d'),
        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1)
    )

    def __init__(self, dataname, **kwargs):
        super().__init__(dataname=dataname, **kwargs)
        self.data = pd.read_csv(dataname, index_col=0, parse_dates=True)
        self.cols = self.data.columns

    def start(self):
        super().start()
        self.order_iter = iter(self.order)
    
    def prenext(self):
        self.next()
    
    def next(self):
        try:
            o, h, l, c, v = next(self.order_iter)
        except StopIteration:
            return
        self.lines.open[0] = o
        self.lines.high[0] = h
        self.lines.low[0] = l
        self.lines.close[0] = c
        self.lines.volume[0] = v
