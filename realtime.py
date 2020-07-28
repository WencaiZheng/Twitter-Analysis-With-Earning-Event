import main.get_raw_tweets as grt
import main.analysis_main as analysis
import main.realtime_tweets as rtt
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
    grt.RawTweet(recent_days = 1).get_multiple_dates(keyword_list)
    # analysis parameters
    flag_paras = {
        'is_save_senti' : 1 ,# whether or not to save the result
        'is_plot' : 0, # plot the graph or not
        'is_log': 0, # log-scale or not
        'is_earning_release' : 0, #get earning relearse date and plot it
        'is_stockprice' : 0, # no stock processing would be much faster

        'is_preopen': 1,
        'is_sendemail': 0,
        'email_addrs_list': ['ml6684@nyu.edu','rangerrod1@gmail.com'],#""
        'ticker' : None,
        'flr_thres' : 5 # follower threshold
    }
    analysis.analysis_ticker(keyword_list,**flag_paras)
    

def Function2():
    """real time update for the large twitter volume ticker
    """
    rtt.RealTimeTweet.run_main()

if __name__ == "__main__":
    keyword_list = ['$WBA','$BDX','$FCX','$MCD','$MSFT','$SWBI','$SQ','$ROKU','$TSLA','$DIS','$BABA','$WMT']#
    Function2()


    pass



    

    
