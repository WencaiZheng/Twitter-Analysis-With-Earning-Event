import os
import pandas as pd
from plotly.subplots import make_subplots
from datetime import timedelta,datetime,date
import plotly.graph_objects as go


import processor._load_intraday as load_intraday
import news._news_yh as news_yh
import news._news_sa as news_sa


class TwitterPlot:
    """This is a class using plotly to plot graph
    """
    def __init__(self,key_word_):
        self.key_word =  key_word_
        self.today = str(date.today())
        self.saveaddr = f'data\\senti_graph\\{self.today}'

    def plot_senti1(self,hourly_ohlc,all_sentis,earning_release_within):
        #self define earning
        #earning_release_within.index =pd.DataFrame()
        #earning_release_within[pd.to_datetime('2020-02-02 16:00:00')]=0

        # plot it with plotly
        fig = make_subplots(rows=4, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[1.5, 1, 1, 1])
        fig.add_trace(go.Ohlc(
            x=hourly_ohlc.index,
            open=hourly_ohlc.open, 
            high=hourly_ohlc.high,
                                
            low=hourly_ohlc.low, 
            
            close=hourly_ohlc.close,
            
            name="Intraday stock price"),
                    row=1, col=1)
        fig.add_trace(go.Bar(
            x=hourly_ohlc.index, 
            y=hourly_ohlc.volume,
            name="Intraday volume",
            marker_color="lightslategray"),
                row=2, col=1)
        '''
        #PLOT the earning
        fig.add_trace(go.Scatter(
            x=earning_release_within.index, 
            y=earning_release_within.Surprise,
            name="Earning Event",
            marker_color="green"),
                row=3, col=1)
        '''
        # plot the sentiment counts
        fig.add_trace(go.Bar(

            x=all_sentis.index, 

            y=all_sentis.All_counts,

            name="Publication count",
            
            marker_color="orange"),
                    row=3, col=1)

        fig.add_trace(go.Bar(

            x=all_sentis.index, 

            y=all_sentis.Positive,

            name="Positive score",
            
            marker_color="green"),
                    row=4, col=1)


        fig.add_trace(go.Bar(
            
            x=all_sentis.index, 
            
            y=all_sentis.Negative,
            
            name="Negative score",
            
            marker_color="red"),

                    row=4, col=1)

        fig.update(layout_xaxis_rangeslider_visible=False)
        # mark the weekends in the plot
        wkds_list=  TwitterPlot.mark_weekend(all_sentis.index)
        """
        # try to include all the weekends in the graph
        shapes=[]
        for wkds in wkds_list:

            shapes.append(
            
            dict(
            type="rect",
            # x-reference is assigned to the x-values
            xref="x",
            # y-reference is assigned to the plot paper [0,1]
            yref="paper",
            x0=wkds[0],
            y0=0,
            x1=wkds[1],
            y1=1,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
            ),
        )
        """
        fig.update_layout(
            
            shapes=[
                # 1st highlight earning
                dict(
                    type="rect",
                    xref="x",
                    yref="paper",
                    x0=earning_release_within.index[0],
                    y0=0,
                    x1=earning_release_within.index[0]+timedelta(hours=1),
                    y1=1,
                    fillcolor="darkviolet",
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                    ),
                    
                # last weekends in all dates we have
                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="paper",
                    x0=wkds_list[-1][0],
                    y0=0,
                    x1=wkds_list[-1][1],
                    y1=1,
                    fillcolor="LightSalmon",
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                    ),
                
            ]
        
        )


        # title
        fig.update_layout(height=600, width=1200,
                        title_text=f"{self.key_word} intraday twitter sentiment and earnings info")

        fig.show()

        # save the plot
        if not os.path.exists(self.saveaddr):os.mkdir(self.saveaddr)
        fig.write_image(f'{self.saveaddr}\\{self.key_word}.png')

    def plot_senti2(self,all_sentis,earning_release_within):
        # plot it with plotly
        fig = make_subplots(rows=3, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[2, 1, 1])
                            
        fig.add_trace(go.Bar(
            x=all_sentis.index, 
        
            y=all_sentis.All_counts,
            
            name="Publication count",
            
            marker_color="lightslategray"),
                    row=1, col=1)

        fig.add_trace(go.Scatter(
            
            x=earning_release_within.index, 
            
            y=earning_release_within.Surprise,
            
            name="Earning Event",
            
            marker_color="green"),
                row=2, col=1)

        fig.add_trace(go.Bar(
            
            x=all_sentis.index, 
            
            y=all_sentis.Positive,
            
            name="Positive score",
            
            marker_color="green"),
                    row=3, col=1)

        fig.add_trace(go.Bar(
            
            x=all_sentis.index, 
            
            y=all_sentis.Negative,
            
            name="Negative score",
            
            marker_color="red"),

                    row=3, col=1)

        # mark the weekends in the plot
        wkds_list =  TwitterPlot.mark_weekend(all_sentis.index)

        fig.update_layout(
            
            shapes=[
                # 1st highlight earning
                dict(
                    type="rect",
                    xref="x",
                    yref="paper",
                    x0=earning_release_within.index[0],
                    y0=0,
                    x1=earning_release_within.index[0]+timedelta(hours=1),
                    y1=1,
                    fillcolor="darkviolet",
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                    ),
                    
                # last weekends in all dates we have
                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="paper",
                    x0=wkds_list[-1][0],
                    y0=0,
                    x1=wkds_list[-1][1],
                    y1=1,
                    fillcolor="LightSalmon",
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                    ),
            ]
        
        )
        
        #title
        fig.update_layout(height=600, width=1200,
                        title_text="{0} intraday twitter sentiment".format(self.key_word))


        fig.show()

        if not os.path.exists(self.saveaddr):os.mkdir(self.saveaddr)
        fig.write_image(f'{self.saveaddr}\\{self.key_word}.png')

    def plot_senti3(self,hourly_ohlc,all_sentis):
        # plot it with plotly
        fig = make_subplots(
            
            rows=4, cols=1,
                            
            shared_xaxes=True, 
                            
            vertical_spacing=0,
                
            row_heights=[1.5, 1, 1, 1])

        fig.add_trace(go.Ohlc(
            
            x=hourly_ohlc.index,
            
            open=hourly_ohlc.open, 
            
            high=hourly_ohlc.high,
            
            low=hourly_ohlc.low, 
            
            close=hourly_ohlc.close,
            
            name="Intraday stock price"),
                    row=1, col=1)

        fig.add_trace(go.Bar(
            
            x=hourly_ohlc.index,
            
            y=hourly_ohlc.volume,
            
            name="Intraday volume", 
            
            marker_color="lightslategray"),
                    
                    row=2, col=1)

        fig.add_trace(go.Bar(
            
            x=all_sentis.index, 
        
            y=all_sentis.All_counts,
            
            name="Publication count",
            
            marker_color="orange"),
                    row=3, col=1)

        fig.add_trace(go.Bar(
            
            x=all_sentis.index, 
            
            y=all_sentis.Positive,
            
            name="Positive score",
            
            marker_color="green"),
                    row=4, col=1)


        fig.add_trace(go.Bar(
            
            x=all_sentis.index, 
            
            y=all_sentis.Negative,
            
            name="Negative score",
            
            marker_color="red"),
                    row=4, col=1)

        fig.update(layout_xaxis_rangeslider_visible=False)

        wkds_list =  TwitterPlot.mark_weekend(all_sentis.index)


        fig.update_layout(
            
            shapes=[
                    
                # last weekends in all dates we have
                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="paper",
                    x0=wkds_list[-1][0],
                    y0=0,
                    x1=wkds_list[-1][1],
                    y1=1,
                    fillcolor="LightSalmon",
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                    ),
            ]
        
        )

        fig.update_layout(height=600, width=1200,
                        title_text="{0} intraday twitter sentiment and earnings info".format(self.key_word))

        fig.show()

        if not os.path.exists(self.saveaddr):os.mkdir(self.saveaddr)
        fig.write_image(f'{self.saveaddr}\\{self.key_word}.png')

    def plot_senti4(self,all_sentis):
        # plot it with plotly
        fig = make_subplots(rows=2, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[1,1])


        fig.add_trace(go.Bar(
            
            x=all_sentis.index, 
            
            y=all_sentis.All_counts,
            
            name="Publication count",
            
            marker_color="lightslategray"),
                    row=1, col=1)

        fig.add_trace(go.Bar(
            
            x=all_sentis.index, 
            
            y=all_sentis.Positive,
            
            name="Positive count",
            
            marker_color="green"),
                    row=2, col=1)

        fig.add_trace(go.Bar(
            
            x=all_sentis.index, 
            
            y=all_sentis.Negative,
            
            name="Negative count",
            
            marker_color="red"),
                    row=2, col=1)

        wkds_list =  TwitterPlot.mark_weekend(all_sentis.index)

        fig.update_layout(
            
            shapes=[
                    
                # last weekends in all dates we have
                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="paper",
                    x0=wkds_list[-1][0],
                    y0=0,
                    x1=wkds_list[-1][1],
                    y1=1,
                    fillcolor="LightSalmon",
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                    ),
            ]
        
        )

        fig.update_layout(height=600, width=1200,
                        title_text="{0} intraday twitter sentiment".format(self.key_word))

        fig.show()

        if not os.path.exists(self.saveaddr):os.mkdir(self.saveaddr)
        fig.write_image(f'{self.saveaddr}\\{self.key_word}.png')
    
    
    def plot_preopen_senti(self,senti_result):
        #plot preopening sentiment
        fig = make_subplots(rows=2, cols=1,
                            shared_xaxes=True, 
                            vertical_spacing=0,row_heights=[1,1])

        fig.add_trace(go.Bar(
            
            x=senti_result.index, 
            
            y=senti_result.user_score,
            
            name="User Weighted Score",
            
            marker_color="lightslategray"),

                    row=1, col=1)
                    

        fig.add_trace(go.Bar(
            
            x=senti_result.index, 
            
            y=senti_result.Positive,
            
            name="Positive count",
            
            marker_color="green"),
                    row=2, col=1)

        fig.add_trace(go.Bar(
            
            x=senti_result.index, 
            
            y=senti_result.Negative,
            
            name="Negative count",
            
            marker_color="red"),
                    row=2, col=1)


        fig.update_layout(height=600, width=1200,
                        title_text=f"{self.key_word} pre-opening twitter sentiment")
        #fig.show()
        #save the graph
        saveaddr = f'data\\preopen\\{self.today}'
        if not os.path.exists(saveaddr):os.mkdir(saveaddr)
        fig.write_image(f'{saveaddr}\\{self.key_word}.png')


    @staticmethod
    def get_earning_within(ticker,all_sentiments):
        """search the earning events within the analysis date and 1 week after
        """
        past_earning_time = news_sa.get_earning_news('NFLX','revenue')
        earning_release_within = pd.DataFrame(columns=["EstimatedEPS","ReportedEPS","Surprise"])
        # add earnings date
        earning_release = news_yh.get_earnings_info(ticker)
        ## get the range date
        
        for edate in earning_release.index:


            if edate < (all_sentiments.index[-1] + timedelta(days = 7))  and edate > all_sentiments.index[0]:
                if edate.hour==0:
                    edate = pd.to_datetime(str(edate.date()-timedelta(days = 1))+' 16:00:00')
                else:
                    edate = pd.to_datetime(str(edate.date())+' 16:05:00')
                earning_release_within.loc[edate,:] = [0,0,0]
                break

        return earning_release_within

    @staticmethod
    def mark_weekend(datetimes):
        #pre process
        dates = sorted(list(set([pd.to_datetime(str(x.date())) for x in datetimes])))
        # initialize
        start_wkd,end_wkd=None,None
        weekend_list = []
        for dat in dates:
            day_num =  dat.weekday()
            if day_num== 5:
                start_wkd = dat
            elif day_num== 0:
                end_wkd = dat
            if start_wkd is not None and end_wkd is not None:
                if end_wkd>start_wkd:
                    weekend_list.append([start_wkd,end_wkd])
                    start_wkd,end_wkd=None,None
                else:
                    end_wkd=None

        return weekend_list


    

if __name__ == "__main__":
    #TwitterPlot.get_earning_within('NFLX','.')
    earning_release_within = pd.DataFrame({pd.to_datetime('2020-02-02 16:00:00'):0})
    #TwitterPlot.mark_weekend([pd.to_datetime('2020-09-25')])
    pass