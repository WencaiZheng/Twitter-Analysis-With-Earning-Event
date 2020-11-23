
import pandas as pd
save_path = 'data\\stock_data\\'


def get_hourly_price(ticker):
    # intraday data from wrds TAQ
    print(f"Processing intraday price for {ticker}")
    stock_price = pd.read_csv(f'{save_path}{ticker}.csv')
    stock_price = stock_price[stock_price.SYM_SUFFIX.isna()]
    stock_price.index = pd.to_datetime(stock_price.DATE.astype(str) + ' ' + stock_price.TIME_M.astype(str))
    # group by hour
    hourly_ohlc=stock_price['PRICE'].resample('1H').ohlc()
    hourly_ohlc['volume'] = stock_price.SIZE.resample('1H').sum()
    return hourly_ohlc

def get_hourly_ratio(ticker):
    # intraday data from wrds TAQ
    print(f"Processing intraday price for {ticker}")
    stock_price = pd.read_csv(f'{save_path}{ticker}.csv')
    stock_price = stock_price[stock_price.SYM_SUFFIX.isna()]
    stock_price.index = pd.to_datetime(stock_price.DATE.astype(str) + ' ' + stock_price.TIME_M.astype(str))
    # group by hour
    hourly=stock_price['PRICE'].resample('1H').mean()
    hourly_r = hourly/hourly.iloc[0]
    # hourly_r['volume'] = stock_price.SIZE.resample('1H').sum()
    return hourly_r