import main.get_raw_tweets as grt
import main.analysis_main as analysis
import news._news_sa as news_sa
import os

os.chdir('C:\\Users\\wenca\\Desktop\\GitRepo\\Twitter-Analysis-With-Earning-Event\\')

def Function1():
    """ Function 1: get raw tweets about keywords and store them analyze twitter sentiment result
    """
    keyword_list = ['$WBA','$BDX','$FCX','$MCD','$MSFT','$SWBI','$SQ','$ROKU','$TSLA','$DIS','$BABA','$WMT']#
    # scraper
    #grt.RawTweet(recent_days = 1).get_multiple_dates(keyword_list)
    # analysis parameters
    flag_paras = {
        'is_save_senti' : 1 ,# whether or not to save the result
        'is_plot' : 0, # plot the graph or not
        'is_log': 0, # log-scale or not
        'is_earning_release' : 0, #get earning relearse date and plot it
        'is_stockprice' : 0, # no stock processing would be much faster
        'is_preopen': 1,
        'is_sendemail': 1,

        'email_addrs': 'wz1298@nyu.edu',
        'ticker' : 'DAL',
        'flr_thres' : 5 # follower threshold
    }
    analysis.analysis_ticker(keyword_list,**flag_paras)
    

def Function2():
    """ Function 3: get news from specific 30 major new press twitter accounts and analyze key word
    analyze and visualize result from function3
    """
    grt.RawTweet(recent_days=7).get_from_news(savename='corona-2020-07-04') # get recent 3 days news from all 30 major press
    key_word_list = ['CORONA','COVID','PANDEMIC']
    analysis.analysis_news(key_word_list,'SPY2',readname='corona-2020-07-04')
    

def Function3():
    
    """ Function 4: get ticker names having earnings next few days
    """
    news_sa.get_earning_names(recent_day = 7,index_code = "RU3") # next 5 days RU3000/SP500 list name

if __name__ == "__main__":
    Function1()
    #Function2()
    # Function3()


    pass



    

    
