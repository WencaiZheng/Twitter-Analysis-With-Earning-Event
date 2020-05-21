import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
import re
from glob import glob
import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import earnings_scraper
import os

################################## parameters needed

key_word ="$BABA" #"SBUX" #TTWO, "TGT","WMT",
ticker = 'BABA'
influencer_threshold = 100 # define influencer with follower
log_scale_flag= 1 # log-scale or not
show_stock_flag = 1 # no stock processing would be much faster
save_senti_flag = 1 # if 1, it saves the sentiment text files by date and positivity 
earning_release_flag = 0
#################################


def effective_ttr(xfile):
    if len(xfile)==0:return None
    xfile["Datetime"] =pd.to_datetime(xfile.Created)
    xfile["Hour"] = xfile.Datetime.dt.hour
    xfile=xfile.sort_values(by="Datetime")
    # filter the effective user twitter
    x_effc = xfile[xfile.User_flr>=influencer_threshold]
    x_effc.index = range(len(x_effc))
    return x_effc

def get_senti(rawtxt):
    txt = rawtxt.upper()
    txt_list= txt.split(" ")
    pos_count,neg_count =0,0
    for i in txt_list:
        if i in pos_dic:pos_count+=1
        if i in neg_dic:neg_count+=1
    # positive
    if pos_count>neg_count:senti = 1
    elif pos_count<neg_count:senti = -1
    else: senti = 0
    return senti

def senti_count(e_file,log_flag):

    """count how many positive or negative in a file named e_file
        log_flag: whether or not scale the count into log
    """
    if e_file is None:return None
    sentis = list(map(get_senti,e_file.Text))
    e_file["Sentiment"] = sentis
    # one hot encoding
    sentis_df = pd.get_dummies(sentis)
    temp=pd.DataFrame([[0]*3]*len(sentis_df),columns=[-1,0,1])
    sentis_df = (temp+sentis_df).fillna(0)
    sentis_df.columns=["Negative","Unknown","Positive"]
    # s_file gives each ttr sentiment
    s_file = e_file.join(sentis_df)

    # change time zone from utc to est
    s_file["EST"] = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in s_file.Datetime]
    s_file.index = list(map(lambda x:x.replace(tzinfo=None),s_file["EST"]))

    # add all sentis get a count 
    s_file["All_counts"] = [1]*len(s_file)
    # count the hourly negative or positive ttr 
    partly_count = s_file.groupby(by="Hour").sum().loc[:,["Negative","Positive","All_counts"]]
    #scale it
    if log_flag:partly_count = np.log(partly_count+1)
    x_zero = pd.Series(24*[0])
    # fill the non-data zone as nan
    hour_count = pd.concat([partly_count,x_zero],axis=1).fillna(0).drop(columns=[0])
    # show negative times in nagative
    hour_count.Negative = -hour_count.Negative
    # save negative or positive tweets v5/5/20:
    save_file = s_file.loc[:,["EST","User_name","Text","Sentiment","Created","User_flr"]]
    pos_tweets = save_file[save_file.Sentiment==1]
    neg_tweets = save_file[save_file.Sentiment==-1]
    return hour_count,pos_tweets,neg_tweets

def get_all_senti(files,pos_dic,neg_dic,log_flag):
    dates = [i[-14:-4] for i in files]
    # count sentiments
    all_sentis = pd.DataFrame()
    for i in range(len(dates)):
        idate = dates[i]
        ifile = files[i]
        xfile=pd.read_csv(ifile)
        # if empty, goes to next date file
        if len(xfile)==0:
            print("file is empty for {0}".format(idate))
            continue 

        e_file = effective_ttr(xfile)
        isenti,pos_tweets,neg_tweets = senti_count(e_file,log_flag)
        isenti.index = list(map(lambda x:pd.to_datetime(idate+" "+str(x)+":00:00"),isenti.index))
        all_sentis = pd.concat([all_sentis,isenti])
        # save the divided files if necessary
        if save_senti_flag:
            senti_path = "results\\{0}".format(key_word)
            if not os.path.exists(senti_path):os.makedirs(senti_path)
            pos_tweets.to_csv(senti_path+"\\{0}_{1}_pos.csv".format(key_word,idate))
            neg_tweets.to_csv(senti_path+"\\{0}_{1}_neg.csv".format(key_word,idate))
        
    print("sentiment files are saved successfully")
    all_sentis = all_sentis.replace([np.inf,-np.inf],[np.nan,np.nan])
    # convert all_sentis from UTC time to EST time
    all_sentis["EST"] = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in all_sentis.index]
    all_sentis.index = list(map(lambda x:x.replace(tzinfo=None),all_sentis["EST"]))
    # add net sentiment
    all_sentis["NetSentiment"] = all_sentis.Positive + all_sentis.Negative

    return all_sentis

def get_hourly_price(ticker):
    # intraday data from wrds TAQ
    print("Processing intraday price for {}".format(ticker))
    stock_price = pd.read_csv("data/{0}.csv".format(ticker))
    stock_price.index = list(map(lambda x,y:pd.to_datetime(str(x)+" "+y),stock_price.DATE,stock_price.TIME_M))
    # group by hour
    hourly_ohlc=stock_price['PRICE'].resample('1H').ohlc()
    return hourly_ohlc

def my_dict(LM_dic):
    pos_dic = LM_dic[LM_dic.Positive!=0].Word.values
    neg_dic = LM_dic[LM_dic.Negative!=0].Word.values
    return pos_dic,neg_dic

def plot_senti(hourly_ohlc,all_sentis,earning_release_within):
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
                    title_text="{0} intraday twitter sentiment and earnings info".format(key_word))
    fig.show()

def plot_pure_senti(all_sentis,earning_release_within):
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
                    title_text="{0} intraday twitter sentiment".format(key_word))
    fig.show()


if __name__ == "__main__":
    ####set path
    result_path = "twitters\\"+key_word+"\\"
    # read all files
    files=glob(result_path+"*"+key_word+"*")
    # see all files'dates
    dates = [i[-14:-4] for i in files]
    print("We are observing data from {0} to {1} for {2}".format(dates[0],dates[-1],key_word))
    # read the sentiment dictionary, predownloaded
    LM_dic = pd.read_csv("dictionary\\LoughranMcDonald_MasterDictionary_2018.csv")
    pos_dic,neg_dic = my_dict(LM_dic)

    # get all sentiment from all files, each file represent a day
    all_sentiments  = get_all_senti(files,pos_dic,neg_dic,log_flag=log_scale_flag)
    if earning_release_flag:
        # add earnings date
        earning_release = earnings_scraper.get_earnings_info(key_word)
        ## get the range date
        earning_release_within= earning_release.join(all_sentiments).dropna()
    else:
        earning_release_within = pd.DataFrame(columns=["Surprise"])
    if show_stock_flag:
        ### read stock data, predownloaded from wrds
        hourly_ohlc = get_hourly_price(ticker)
        ### plot the graph
        plot_senti(hourly_ohlc,all_sentiments,earning_release_within)
    else:
        plot_pure_senti(all_sentiments,earning_release_within)