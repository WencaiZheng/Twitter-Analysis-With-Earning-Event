import main.scraper_main as scraper_main
import main.analysis_main as analysis_main
import main.news_main as news_main
import news.news_sa as news_sa
# scraper parameters
key_words = ['$NKE']
recent_days = 7
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

if __name__ == "__main__":
    """ Function 1: get raw tweets and store them
    """
    scraper_main.RawTweet(key_words,recent_days,"en").get_multiple_dates()

    """ Function 2: analyze them
    """
    analysis_main.analysis_ticker(key_word,ticker,flr_thres,**flag_paras)

    """ Function 3: get news from specific 30 major new press twitter accounts and analyze key word
    """
    # news_main.get_news(3) # get recent 3 days news from all 30 major press
    # news_main.analysis_news()

    """ Function 4: get ticker names having earnings next few days
    """
    # news_sa.get_earning_names(recent_day = 5,index_code = "RU3") # next 5 days RU3000 list name
