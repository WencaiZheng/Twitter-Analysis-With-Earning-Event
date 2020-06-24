
import pandas as pd
save_path = 'data\\stock_data\\'
def get_hourly_price(ticker):
    # intraday data from wrds TAQ
    print(f"Processing intraday price for {ticker}")
    stock_price = pd.read_csv(f'{save_path}{ticker}.csv')
    stock_price = stock_price[stock_price.SYM_SUFFIX.isna()]
    stock_price.index = list(map(lambda x,y:pd.to_datetime(str(x)+" "+y),stock_price.DATE,stock_price.TIME_M))
    # group by hour
    hourly_ohlc=stock_price['PRICE'].resample('1H').ohlc()
    hourly_ohlc['volume'] = stock_price.SIZE.resample('1H').sum()
    return hourly_ohlc