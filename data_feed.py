import pandas as pd
import backtrader as bt
from binance.client import Client
import datetime as dt


class MyDataFeed(bt.feeds.PandasData):
    """
    Define custom data feed to be used with backtrader.
    """
    params = (
        ('datetime', None),
        ('open', 'Open'),
        ('high', 'High'),
        ('low', 'Low'),
        ('close', 'Close'),
        ('volume', 'Volume'),
        ('openinterest', None)
    )


def download_data(symbol, interval, start_date, end_date):
    """
    Downloads historical OHLCV data from the Binance API and returns a Pandas DataFrame.

    Parameters:
    symbol (str): The trading symbol to download data for (e.g. 'BTCUSDT').
    interval (str): The time interval to use for the data (e.g. '1d' for daily data, '1h' for hourly data).
    start_date (str): The start date for the data in the format 'YYYY-MM-DD'.
    end_date (str): The end date for the data in the format 'YYYY-MM-DD'.

    Returns:
    df (pd.DataFrame): A Pandas DataFrame containing the downloaded data.
    """
    client = Client()

    # Convert start and end dates to timestamps
    start_date = int(dt.datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
    end_date = int(dt.datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)

    # Download data from Binance API
    klines = client.futures_klines(symbol=symbol, interval=interval, startTime=start_date, endTime=end_date)

    # Convert data to Pandas DataFrame
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Clean up DataFrame
    df.drop(['close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'], axis=1, inplace=True)
    df.set_index('timestamp', inplace=True)
    df = df.astype(float)

    return df


def resample_ohlcv(df, timeframe):
    """
    Resample OHLCV data to a specified timeframe.
    """
    ohlc_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }

    return df.resample(timeframe).apply(ohlc_dict)


def fill_missing_values(df):
    """
    Fill missing OHLCV data using forward-fill.
    """
    df.fillna(method='ffill', inplace=True)


def preprocess_data(df, timeframe):
    """
    Preprocess OHLCV data.
    """
    # Resample data
    df_resampled = resample_ohlcv(df, timeframe)

    # Fill missing data
    fill_missing_values(df_resampled)

    return df_resampled


def create_data_feed(symbol, interval, start_date, end_date, timeframe):
    """
    Create and return an instance of MyDataFeed using data downloaded from the Binance API.

    Parameters:
    symbol (str): The trading symbol to download data for (e.g. 'BTCUSDT').
    interval (str): The time interval to use for the data (e.g. '1d' for daily data, '1h' for hourly data).
    start_date (str): The start date for the data in the format 'YYYY-MM-DD'.
    end_date (str): The end date for the data in the format 'YYYY-MM-DD'.
    timeframe (str): The timeframe to resample the data to (e.g. '1D' for daily data, '4H' for 4-hourly data).

    Returns:
    data_feed (MyDataFeed): An instance of MyDataFeed containing the downloaded and preprocessed data.
    """

    # Download data
    df = download_data(symbol, interval, start_date, end_date)

    # Preprocess data
    df_processed = preprocess_data(df, timeframe)

    # Create data feed
    data_feed = MyDataFeed(dataname=df_processed)

    return data_feed
