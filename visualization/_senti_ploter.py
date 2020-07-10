import os
import pandas as pd
from plotly.subplots import make_subplots
from datetime import timedelta,datetime,date
import plotly.graph_objects as go


import processor._load_intraday as load_intraday
import news._news_yh as news_yh



class TwitterPlot:

    def __init__(self,key_word_):
        self.key_word =  key_word_
        self.today = str(date.today())

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
        fig.add_trace(go.Scatter(x=earning_release_within.index, y=earning_release_within.Surprise,name="Earning Event",marker_color="green"),
                row=2, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Positive,name="Positive count",marker_color="green"),
                    row=3, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Negative,name="Negative count",marker_color="red"),
                    row=3, col=1)
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(height=600, width=1200,
                        title_text="{0} intraday twitter sentiment and earnings info".format(self.key_word))
        fig.show()

    def plot_senti2(self,all_sentis,earning_release_within):
        # plot it with plotly
        fig = make_subplots(rows=3, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[3, 1.5, 1])
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.All_counts,name="Publication count",marker_color="lightslategray"),
                    row=1, col=1)
        fig.add_trace(go.Scatter(x=earning_release_within.index, y=earning_release_within.Surprise,name="Earning Event",marker_color="green"),
                row=2, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.NetSentiment,name="Net Sentiment",marker_color="brown"),
                row=2, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Positive,name="Positive count",marker_color="green"),
                    row=3, col=1)
        fig.add_trace(go.Bar(x=all_sentis.index, y=all_sentis.Negative,name="Negative count",marker_color="red"),
                    row=3, col=1)
        fig.update_layout(height=600, width=1200,
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
        fig.update_layout(height=600, width=1200,
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
        fig.update_layout(height=600, width=1200,
                        title_text="{0} intraday twitter sentiment".format(self.key_word))
        fig.show()
    
    
    def plot_preopen_senti(self,senti_result):
        #plot preopening sentiment
        fig = make_subplots(rows=2, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[1,1])

        fig.add_trace(go.Bar(x=senti_result.index, y=senti_result.user_score,name="User Weighted Score",marker_color="lightslategray"),
                    row=1, col=1)
                    
        fig.add_trace(go.Bar(x=senti_result.index, y=senti_result.Sentiment,name="Pure Sentiment",marker_color="red"),
                    row=2, col=1)

        fig.update_layout(height=600, width=1200,
                        title_text=f"{self.key_word} pre-opening twitter sentiment")
        #fig.show()
        #save the graph
        saveaddr = f'data\\preopen\\{self.today}'
        if not os.path.exists(saveaddr):os.mkdir(saveaddr)
        fig.write_image(f'{saveaddr}\\{self.key_word}.png')

    @staticmethod
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

    @staticmethod
    def get_earning_within(ticker,all_sentiments):
        """search the earning events within the analysis date and 1 week after
        """
        earning_release_within = pd.DataFrame(columns=["EstimatedEPS","ReportedEPS","Surprise"])
        # add earnings date
        earning_release = news_yh.get_earnings_info(ticker)
        ## get the range date
        for edate in earning_release.index:
            if edate < (all_sentiments.index[-1] + timedelta(days = 7))  and edate > all_sentiments.index[0]:
                if edate.hour==0:
                    edate = pd.to_datetime(str(edate.date()-timedelta(days = 1))+' 16:00:00')
                else:
                    edate = pd.to_datetime(str(edate.date())+' 16:00:00')
                earning_release_within.loc[edate,:] = [0,0,0]
                break

        return earning_release_within


def plotit(key_word,ticker,all_sentiments,show_stock_flag,earning_release_flag):
    
    if earning_release_flag and show_stock_flag:
        earning_release_within = TwitterPlot.get_earning_within(ticker,all_sentiments)
        ### read stock data, predownloaded from wrds
        hourly_ohlc = load_intraday.get_hourly_price(ticker)
        ### plot the graph
        TwitterPlot(key_word).plot_senti1(hourly_ohlc,all_sentiments,earning_release_within)

    elif earning_release_flag and not show_stock_flag:
        earning_release_within = TwitterPlot.get_earning_within(ticker,all_sentiments)
        TwitterPlot(key_word).plot_senti2(all_sentiments,earning_release_within)
        
    elif show_stock_flag and not earning_release_flag:
        ### read stock data, predownloaded from wrds
        hourly_ohlc = load_intraday.get_hourly_price(ticker)
        ### plot the graph
        TwitterPlot(key_word).plot_senti3(hourly_ohlc,all_sentiments)

    else:
        TwitterPlot(key_word).plot_senti4(all_sentiments)

    

if __name__ == "__main__":
    pass