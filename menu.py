import main.scraper_main as scraper_main
import main.analysis_main as analysis_main
import main.news_main as news_main
import news.news_sa as news_sa

def Function1():
    """ Function 1: get raw tweets and store them
    """
    key_word_list = ['$NKE']
    recent_days = 3
    # scraper
    scraper_main.RawTweet(key_word_list,recent_days,"en").get_multiple_dates()
    
def Function2():
    """ Function 2: analyze twitter result from function 1
    """
    # analysis parameters
    key_word = '$NKE' # PLCE $LULU $PLAY $JW.A 
    ticker = 'NKE'
    flr_thres = 0 # follower threshold
    flag_paras = {
        'is_save_senti' : 1 ,# whether or not to save the result
        'is_plot' : 1, # plot the graph or not
        'is_log': 0, # log-scale or not
        'is_earning_release' : 1,
        'is_show_stock' : 1 #is_ no stock processing would be much faster
    }
    analysis_main.analysis_ticker(key_word,ticker,flr_thres,**flag_paras)

def Function3():
    """ Function 3: get news from specific 30 major new press twitter accounts and analyze key word
    """
    news_main.get_news(8) # get recent 3 days news from all 30 major press

def Function4():
    """ Function 5: analyze and visualize result from function3
    """
    key_word_list = ['CORONA','COVID','PANDEMIC']
    news_main.analysis_news(key_word_list,'SPY','corona-2020-06-26.csv')

def Function5():
    """ Function 4: get ticker names having earnings next few days
    """
    news_sa.get_earning_names(recent_day = 30,index_code = "SP5") # next 5 days RU3000/SP500 list name

if __name__ == "__main__":
    # Function1()
    # Function2()
    #Function3()
    # Function4()
    Function5()




    

    
