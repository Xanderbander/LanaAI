import backtrader as bt
import pandas as pd

class CustomData(bt.feeds.PandasData):
    lines = ('open', 'high', 'low', 'close')

    params = (
        ('open', 'Open'),
        ('high', 'High'),
        ('low', 'Low'),
        ('close', 'Close'),
        ('volume', 'Volume'),
    )

    def __init__(self, dataname, **kwargs):
        df = pd.read_csv(dataname, parse_dates=True, index_col='Date')
        super().__init__(dataname=dataname, dataframe=df, **kwargs)

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=20
        )

    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy(size=1)
        elif self.data.close[0] < self.sma[0]:
            self.sell(size=1)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    data = CustomData(dataname='my_data.csv')
    cerebro.adddata(data)

    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
    print('Starting Portfolio Value: ${}'.format(cerebro.broker.getvalue()))

    cerebro.run()

    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - 10000
    print('Final Portfolio Value: ${}'.format(portvalue))
    print('P/L: ${}'.format(pnl))
