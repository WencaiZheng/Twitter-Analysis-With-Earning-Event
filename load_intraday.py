
import pandas as pd

def get_hourly_price(ticker):
    # intraday data from wrds TAQ
    print("Processing intraday price for {}".format(ticker))
    stock_price = pd.read_csv("data/{0}.csv".format(ticker))
    stock_price.index = list(map(lambda x,y:pd.to_datetime(str(x)+" "+y),stock_price.DATE,stock_price.TIME_M))
    # group by hour
    hourly_ohlc=stock_price['PRICE'].resample('1H').ohlc()
    return hourly_ohlc