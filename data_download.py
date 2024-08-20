import pandas as pd
from binance.client import Client
import datetime as dt

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
