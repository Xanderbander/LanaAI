import pandas as pd

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
