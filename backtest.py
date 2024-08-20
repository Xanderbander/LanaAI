import backtrader as bt
import pandas as pd

class MyStrategy(bt.Strategy):
    """
    Define custom strategy for backtrader.
    """
    params = (
        ('maperiod', 15),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.order = self.sell()

def load_data(file_path):
    """
    Load and preprocess data from a CSV file and return a Pandas DataFrame.
    """
    # Read CSV file
    df = pd.read_csv(file_path, index_col=0)

    # Convert index to datetime
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S')

    # Resample to 1 minute timeframe
    df = df.resample('1min').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })

    # Drop rows with missing data
    df.dropna(inplace=True)

    # Add custom indicators to the DataFrame
    df['sma'] = df['close'].rolling(window=15).mean()

    return df

def run_strategy(data):
    """
    Run the backtest using the given data and strategy.
    """
    cerebro = bt.Cerebro()

    # Add the data feed to the backtest
    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    # Add the strategy to the backtest
    cerebro.addstrategy(MyStrategy)

    # Set the commission rate and margin requirements
    cerebro.broker.setcommission(commission=0.001)
    cerebro.broker.setmargin(margin=0.2)

    # Set the starting cash and size of the position
    cerebro.broker.setcash(10000)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

    # Run the backtest
    cerebro.run()

    # Print the final portfolio value
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    # Load and preprocess the data
    data = load_data('my_data.csv')

    # Run the strategy
    run_strategy(data)
