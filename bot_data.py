import pandas as pd
import talib

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

    def get_indicators(self, indicator_list):
        for indicator in indicator_list:
            if indicator == 'SMA':
                self.data['sma'] = self.data['close'].rolling(20).mean()
            elif indicator == 'EMA':
                self.data['ema'] = talib.EMA(self.data['close'], timeperiod=20)
            elif indicator == 'BBANDS':
                upper, middle, lower = talib.BBANDS(self.data['close'], timeperiod=20)
                self.data['bbands_upper'] = upper
                self.data['bbands_middle'] = middle
                self.data['bbands_lower'] = lower
            # Add additional elif statements for more indicators

        return self.data
