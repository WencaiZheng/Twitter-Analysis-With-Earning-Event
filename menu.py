import main.scraper_main as scraper_main
import main.analysis_main as analysis_main
import main.news_main as news_main
import processor.news_sa as news_sa
# scraper parameters
key_words = ['$NKE']
recent_days = 7
# analysis parameters
key_word = '$NKE' # PLCE $LULU $PLAY $JW.A 
ticker = 'NKE'
flr_thres = 0 # follower threshold

flag_paras = {
    'is_save_senti' : 1 ,# whether or not to save the result
    'is_plot' : 1, # plot the graph
    'log_flag': 0, # log-scale or not
    'is_earning_release' : 1,
    'is_show_stock' : 1 # no stock processing would be much faster
}

if __name__ == "__main__":
    # get raw tweets and save them
    scraper_main.RawTweet(key_words,recent_days,"en").get_multiple_dates()
    # analyze them
    analysis_main.analysis_ticker(key_word,ticker,flr_thres,**flag_paras)

    # news main
    # news_main.get_news(3) # get recent 3 days news from all 30 press
    # news_main.analysis_news()

    # get names have earnings next week
    # news_sa.get_earning_names(recent_day = 5,index_code = "RU3") # next 5 days