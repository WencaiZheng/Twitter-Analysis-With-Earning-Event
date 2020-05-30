
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import load_intraday as ghp
import earnings_scraper
import pandas as pd


class TwitterPlot:

    def __init__(self,key_word_):
        self.key_word =  key_word_


    def plot_senti1(self,hourly_ohlc,all_sentis,earning_release_within):
        # plot it with plotly
        fig = make_subplots(rows=3, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[3, 1.5, 1,])
        fig.add_trace(go.Ohlc(x=hourly_ohlc.index,
                                open=hourly_ohlc.open, high=hourly_ohlc.high,
                                low=hourly_ohlc.low, close=hourly_ohlc.close,name="Stock OHLC"),
                    row=1, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.All_counts,name="Publication count",marker_color="lightslategray"),
                    row=2, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.NetSentiment,name="Net Sentiment",marker_color="brown"),
                row=2, col=1)
        fig.add_trace(go.Scatter(x=earning_release_within.index, y=earning_release_within.Surprise,name="Earning Surprise(%)",marker_color="grey"),
                row=2, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Positive,name="Positive count",marker_color="green"),
                    row=3, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Negative,name="Negative count",marker_color="red"),
                    row=3, col=1)
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(height=800, width=1200,
                        title_text="{0} intraday twitter sentiment and earnings info".format(self.key_word))
        fig.show()

    def plot_senti2(self,all_sentis,earning_release_within):
        # plot it with plotly
        fig = make_subplots(rows=3, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[3, 1.5, 1])
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.All_counts,name="Publication count",marker_color="lightslategray"),
                    row=1, col=1)
        fig.add_trace(go.Scatter(x=earning_release_within.index, y=earning_release_within.Surprise,name="Earning Surprise(%)",marker_color="grey"),
                row=1, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.NetSentiment,name="Net Sentiment",marker_color="brown"),
                row=2, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Positive,name="Positive count",marker_color="green"),
                    row=3, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Negative,name="Negative count",marker_color="red"),
                    row=3, col=1)
        fig.update_layout(height=800, width=1200,
                        title_text="{0} intraday twitter sentiment".format(self.key_word))
        fig.show()

    def plot_senti3(self,hourly_ohlc,all_sentis):
        # plot it with plotly
        fig = make_subplots(rows=3, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[3, 1.5, 1,])
        fig.add_trace(go.Ohlc(x=hourly_ohlc.index,
                                open=hourly_ohlc.open, high=hourly_ohlc.high,
                                low=hourly_ohlc.low, close=hourly_ohlc.close,name="Stock OHLC"),
                    row=1, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.All_counts,name="Publication count",marker_color="lightslategray"),
                    row=2, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.NetSentiment,name="Net Sentiment",marker_color="brown"),
                row=2, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Positive,name="Positive count",marker_color="green"),
                    row=3, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Negative,name="Negative count",marker_color="red"),
                    row=3, col=1)
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(height=800, width=1200,
                        title_text="{0} intraday twitter sentiment and earnings info".format(self.key_word))
        fig.show()

    def plot_senti4(self,all_sentis):
        # plot it with plotly
        fig = make_subplots(rows=3, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[3, 1.5, 1])
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.All_counts,name="Publication count",marker_color="lightslategray"),
                    row=1, col=1)

        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.NetSentiment,name="Net Sentiment",marker_color="brown"),
                row=2, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Positive,name="Positive count",marker_color="green"),
                    row=3, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Negative,name="Negative count",marker_color="red"),
                    row=3, col=1)
        fig.update_layout(height=800, width=1200,
                        title_text="{0} intraday twitter sentiment".format(self.key_word))
        fig.show()

def plotit(key_word,ticker,all_sentiments,show_stock_flag,earning_release_flag):

    if earning_release_flag and show_stock_flag:
        # add earnings date
        earning_release = earnings_scraper.get_earnings_info(key_word)
        ## get the range date
        earning_release_within= earning_release.join(all_sentiments).dropna()
        
        ### read stock data, predownloaded from wrds
        hourly_ohlc = ghp.get_hourly_price(ticker)
        ### plot the graph
        TwitterPlot(key_word).plot_senti1(hourly_ohlc,all_sentiments,earning_release_within)

    elif earning_release_flag and not show_stock_flag:
        # add earnings date
        earning_release = earnings_scraper.get_earnings_info(key_word)
        ## get the range date
        earning_release_within= earning_release.join(all_sentiments).dropna()
        TwitterPlot(key_word).plot_senti2(all_sentiments,earning_release_within)
        
    elif show_stock_flag and not earning_release_flag:

        earning_release_within = pd.DataFrame(columns=["Surprise"])
        ### read stock data, predownloaded from wrds
        hourly_ohlc = ghp.get_hourly_price(ticker)
        ### plot the graph
        TwitterPlot(key_word).plot_senti3(hourly_ohlc,all_sentiments)

    else:
        TwitterPlot(key_word).plot_senti4(all_sentiments)


if __name__ == "__main__":
    pass