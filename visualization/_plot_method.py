
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import visualization._plotly_ploter as pp
import processor._load_intraday as load_intraday

def plot_senti(key_word,ticker,all_sentiments,show_stock_flag,earning_release_flag):
    
    if earning_release_flag and show_stock_flag:
        earning_release_within = pp.TwitterPlot.get_earning_within(ticker,all_sentiments)
        ### read stock data, predownloaded from wrds
        hourly_ohlc = load_intraday.get_hourly_price(ticker)
        ### plot the graph
        pp.TwitterPlot(key_word).plot_senti1(hourly_ohlc,all_sentiments,earning_release_within)

    elif earning_release_flag and not show_stock_flag:
        earning_release_within = pp.TwitterPlot.get_earning_within(ticker,all_sentiments)
        pp.TwitterPlot(key_word).plot_senti2(all_sentiments,earning_release_within)
        
    elif show_stock_flag and not earning_release_flag:
        ### read stock data, predownloaded from wrds
        hourly_ohlc = load_intraday.get_hourly_price(ticker)
        ### plot the graph
        pp.TwitterPlot(key_word).plot_senti3(hourly_ohlc,all_sentiments)

    else:
        pp.TwitterPlot(key_word).plot_senti4(all_sentiments)

def plot_news(hourly_ohlc,all_sentis):
    fig = make_subplots(rows=3, cols=1,shared_xaxes=True, 
                    vertical_spacing=0,row_heights=[3, 1, 1])
    fig.add_trace(go.Ohlc(x=hourly_ohlc.index,open=hourly_ohlc.open, high=hourly_ohlc.high,
                            low=hourly_ohlc.low, close=hourly_ohlc.close,name="Stock OHLC"),row=1, col=1)

    fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.values,name=f"Key Word Count",marker_color="lightslategray"),row=2, col=1)

    fig.add_trace(go.Bar(x=hourly_ohlc.index, y=hourly_ohlc.volume,name=f"Stock Volume",marker_color="green"),row=3, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(height=600, width=1200,
                    title_text=f"News intraday twitter sentiment from mainstream media")
    fig.show()