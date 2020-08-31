import re
import os
import datetime
import pandas as pd
import numpy as np
from glob import glob
import warnings

import news._news_yh as news_yh
import visualization._plot_method as senti_ploter
import processor._automail as automail
import processor._senti_process as senti_process
import statistics._twitter_stats as twitter_stats
import processor._load_intraday as load_intraday


warnings.simplefilter("ignore")

def analysis_ticker(keyword_list,is_save_senti,is_plot,is_log,is_earning_release,is_stockprice,is_preopen,is_sendemail,email_addrs_list,ticker,flr_thres):
    for key_word in keyword_list:
        ####set path
        keyword_path = f"data\\raw_twitters\\{key_word}\\" # where the raw twitters are stored
        ticker = key_word.split('$')[-1] # overwrite the ticker name
        # read all files
        files=glob(f'{keyword_path}*{key_word}*')
        #if only need to run the program pre open time, which limit the time from last day 4:00pm to next day 9:30am
        if is_preopen:
            files = files[-2:]
        # see all files'dates
        dates = [i[-14:-4] for i in files]
        print(f'We are observing data from {dates[0]} to {dates[-1]} for {key_word}')
        # get all sentiment from all files, each file represent a day
        all_sentiments  = senti_process.SentiProcess(key_word).get_all_senti(files,flr_thres,is_log,is_save_senti)
        ###################################
        #twitter_stats.show_top(result_path,key_word,topn,is_show_topwds)
        #plot #####################################################
        if is_plot:
            senti_ploter.plot_senti(key_word,ticker,all_sentiments,is_stockprice,is_earning_release)
        
        # statits
        #twitter_stats.observe_annoucement(ticker,all_sentiments)
        #twi_daily = twitter_stats.daily_tweets(all_sentiments)
    if is_preopen:
        twitter_stats.pre_opening_analysis(keyword_list,flr_thres)
        automail.SendEmail(toaddr = email_addrs_list).send_preopen_email()
    if not is_preopen and is_sendemail:
        automail.SendEmail(toaddr = email_addrs_list).send_regular_email()

    pass

def analysis_news(kw_list,ticker,readname):

    # get all sentiment from all files, each file represent a day
    all_sentis  = senti_process.SentiProcess.analysis_news(kw_list,readname)
    #plot #####################################################
    hourly_ohlc = load_intraday.get_hourly_price(ticker)
    senti_ploter.plot_news(hourly_ohlc,all_sentis)
    pass

def analysis_macro(filename):
    #past half tweets from those accounts
    macro_tweet = pd.read_csv(f'data\\macro\\{filename}.csv')
    #
    macro_name = pd.read_csv(f'dictionary\\Macro.csv').iloc[:,0]
    name_df=pd.DataFrame([0]*len(macro_name),index=macro_name)
    tweet_dict = dict()
    for i in macro_name:
        tweet_dict[i]= []
    # iterate each tweet
    for it,tweet in enumerate(macro_tweet.Text):
        # test each keyword
        for imac in macro_name:
            if imac in tweet:
                name_df.loc[imac,0] += 1
                tweet_dict[imac] += (macro_tweet.iloc[it,-3],macro_tweet.iloc[it,-5],macro_tweet.iloc[it,-1])

    top_names = name_df.sort_values(by=0,ascending=False).iloc[:3,0]
    return top_names,tweet_dict

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
    analysis_macro('macrotest1')
    pass