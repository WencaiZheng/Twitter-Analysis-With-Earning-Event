import re
import os
import datetime
import pandas as pd
import numpy as np
from glob import glob
import warnings

import news._news_yh as news_yh
import visualization._senti_ploter as senti_ploter
import processor._senti_process as senti_process
import statistics._twitter_stats as twitter_stats
import processor._fix_dictionary as  mydictionary
import processor._load_intraday as load_intraday

warnings.simplefilter("ignore")
os.chdir(os.getcwd())

def analysis_ticker(key_word,ticker,flr_thres,is_save_senti,is_plot,is_log,is_earning_release,is_show_stock):
    ####set path
    keyword_path = f"data\\raw_twitters\\{key_word}\\" # where the raw twitters are stored
    # read all files
    files=glob(f'{keyword_path}*{key_word}*')
    # see all files'dates
    dates = [i[-14:-4] for i in files]

    print(f'We are observing data from {dates[0]} to {dates[-1]} for {key_word}')

    # read the sentiment dictionary, predownloaded
    pos_dic,neg_dic = mydictionary.TwitterDict().new_dict()
    # get all sentiment from all files, each file represent a day
    all_sentiments  = senti_process.SentiProcess(key_word,pos_dic,neg_dic).get_all_senti(files,flr_thres,is_log,is_save_senti)
    ###################################
    #twitter_stats.show_top(result_path,key_word,topn,is_show_topwds)
    #plot #####################################################
    if is_plot:
        senti_ploter.plotit(key_word,ticker,all_sentiments,is_show_stock,is_earning_release)
    twitter_stats.observe_annoucement(ticker,all_sentiments)
    # statits
    twi_daily = twitter_stats.daily_tweets(all_sentiments)
    twitter_stats.daily_plot(twi_daily)

    pass

def analysis_news(kw_list,ticker,readname):

    # read the sentiment dictionary, predownloaded
    pos_dic,neg_dic = mydictionary.TwitterDict().new_dict()
    # get all sentiment from all files, each file represent a day
    all_sentis  = senti_process.SentiProcess(kw_list,pos_dic,neg_dic).analysis_news(kw_list,ticker,readname)
    #plot #####################################################
    hourly_ohlc = load_intraday.get_hourly_price('SPY')
    senti_ploter.TwitterPlot.plot_news(hourly_ohlc,all_sentis)
    pass

if __name__ == "__main__":
    # parameters
    key_word = '$RAD' # PLCE $LULU $PLAY $JW.A 
    ticker = 'RAD'
    flr_thres = 0

    flag_paras = {
        'is_save_senti' : 1 ,
        'is_plot' : 1, # plot the graph
        'is_log': 0, # log-scale or not
        'is_earning_release' : 1,
        'is_show_stock' : 1 # no stock processing would be much faster
    }
    analysis_ticker(key_word,ticker,flr_thres,**flag_paras)
    pass