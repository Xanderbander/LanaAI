import os
import configparser
import datetime as dt
import backtrader as bt
from my_strategy import MyStrategy

class Config:
    def __init__(self):
        # Initialize configparser to read from config.ini file
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), 'config.ini'))

        # General Settings
        self.data_path = config.get('General', 'data_path')
        self.results_path = config.get('General', 'results_path')
        self.start_date = dt.datetime.strptime(config.get('General', 'start_date'), '%Y-%m-%d')
        self.end_date = dt.datetime.strptime(config.get('General', 'end_date'), '%Y-%m-%d')

        # Strategy Settings
        self.strategy_params = {
            'stop_loss_pct': float(config.get('Strategy', 'stop_loss_pct')),
            'trailing_stop_loss_pct': float(config.get('Strategy', 'trailing_stop_loss_pct'))
        }

        # Broker Settings
        self.cash = float(config.get('Broker', 'cash'))
        self.commission = float(config.get('Broker', 'commission'))

def get_data_feeds(config):
    data_feeds = []

    # Read data from my_data.csv file
    data = bt.feeds.GenericCSVData(
        dataname=os.path.join(os.getcwd(), 'my_data.csv'),
        fromdate=config.start_date,
        todate=config.end_date,
        nullvalue=0.0,
        dtformat=('%Y-%m-%d %H:%M:%S'),
        datetime=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1
    )
    data_feeds.append(data)

    return data_feeds

def run_strategy():
    config = Config()
    cerebro = bt.Cerebro()

    # Add data feeds to Cerebro instance
    data_feeds = get_data_feeds(config)
    for data in data_feeds:
        cerebro.adddata(data)

    # Add strategy to Cerebro instance
    cerebro.addstrategy(MyStrategy, **config.strategy_params)

    # Set broker parameters
    cerebro.broker.setcash(config.cash)
    cerebro.broker.setcommission(commission=config.commission)

    # Run the backtest
    cerebro.run()

    # Print the final portfolio value
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    run_strategy()
