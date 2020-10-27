#!/usr/bin/env python
import main.get_raw_tweets as grt
import main.analysis_main as analysis
# import main.news_main as news_main
import news._news_sa as news_sa
import pandas as pd
import os
#change it to the address where the file is located in your computer
#os.chdir('C:\\Users\\wenca\\Desktop\\GitRepo\\Twitter-Analysis-With-Earning-Event\\')

def Function1(keyword_list):
    """ Function 1: get raw tweets about keywords and store them analyze twitter sentiment result
    """
    # scraper
    keyword_list = ['$'+x for x in keyword_list] #'$'+
    #
    #grt.RawTweet(recent_days = 6).get_multiple_dates(keyword_list)
    # analysis parameters
    flag_paras = {
        'is_save_senti' : 1 ,# whether or not to save the result
        'is_plot' : 1, # plot the graph or not
        'is_log': 0, # log-scale or not
        'is_earning_release' : 1, #get earning relearse date and plot it
        'is_stockprice' : 1, # no stock processing would be much faster

        'is_preopen': 0,
        'is_sendemail': 0,
        'email_addrs_list': ['wz1298@nyu.edu'], 
        'ticker' : None,
        'flr_thres' : 5 # follower threshold
    }
    analysis.analysis_ticker(keyword_list,**flag_paras)
    

def Function2():
    """ Function 2: get news from specific 30 major new press twitter accounts and analyze key word
    analyze and visualize result from function3
    """
    grt.RawTweet(recent_days=7).get_from_accounts('macro',savename='corona-2020-07-21') # get recent 3 days news from all 30 major press
    key_word_list = ['CORONA','COVID','PANDEMIC']
    analysis.analysis_news(key_word_list,'SPY2',readname='corona-2020-07-21')
    

def Function3():
    
    """ Function 3: get ticker names having earnings next few days
    """
    news_sa.save_earning_names(recent_day = 5,index_code = "RU3") # next 5 days RU3000/SP500 list name

if __name__ == "__main__":
    keyword_list = ['PFE' ,'SWK' ,'SHW', 'RTX', 'SPGI']#['DAL','JPM','C','FAST','BLK','JNJ']
    Function1(keyword_list)
    #Function2()    
    #Function3()


    pass



    

    
