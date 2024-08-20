import pandas as pd

class BotData:
    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
        self.data = pd.read_csv(f'data/{self.symbol}_{self.timeframe}.csv')
        self.data['datetime'] = pd.to_datetime(self.data['datetime'])
        self.data.set_index('datetime', inplace=True)

    def get_latest_candle(self):
        return self.data.iloc[-1]

    def get_candles(self, n):
        return self.data.iloc[-n:]

    def add_indicators(self, indicator_list):
        for indicator in indicator_list:
            if indicator == 'SMA':
                self.data['sma'] = self.data['close'].rolling(20).mean()

            # Add your custom indicators here

        return self.data
