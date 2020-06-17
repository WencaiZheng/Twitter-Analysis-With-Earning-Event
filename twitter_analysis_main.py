import datetime
import pandas as pd
import numpy as np
import re
from glob import glob
import os
import news_yh
import senti_ploter
import top_words
import senti_process
import twitter_stats
import mydictionary
import warnings
warnings.simplefilter("ignore")
os.chdir(os.getcwd())
####################          PARAMETERS        #######################
key_word = '$ORCL' # PLCE $LULU $PLAY $JW.A 
ticker = 'ORCL'
# 
save_senti_flag = 1 # if 1, it saves the sentiment text files by date and positivity 
is_show_topwds = 1 ; topn = 20 # show the top words for key words
flr_thres = 20 # define influencer with follower
# plot flags
is_plot = 1 # plot the graph
log_flag= 0 # log-scale or not
is_earning_release = 1
is_show_stock = 0 # no stock processing would be much faster
#########################################################################


if __name__ == "__main__":
    ####set path
    keyword_path = f"twitters\\{key_word}\\" # where the raw twitters are stored
    result_path = f"results\\{key_word}\\" # where the analysis results are stored

    # read all files
    files=glob(f'{keyword_path}*{key_word}*')
    # see all files'dates
    dates = [i[-14:-4] for i in files]

    print(f'We are observing data from {dates[0]} to {dates[-1]} for {key_word}')

    # read the sentiment dictionary, predownloaded
    pos_dic,neg_dic = mydictionary.TwitterDict().new_dict()
    # get all sentiment from all files, each file represent a day
    all_sentiments  = senti_process.SentiProcess(key_word,pos_dic,neg_dic).get_all_senti(files,flr_thres,log_flag,save_senti_flag)
    ###################################
    #########################
    top_words.show_top(result_path,key_word,topn,is_show_topwds)
    #plot #####################################################
    if is_plot:senti_ploter.plotit(key_word,ticker,all_sentiments,is_show_stock,is_earning_release)
    # statits
    twi_daily = twitter_stats.daily_tweets(files)
    print(twi_daily)
    #plt.plot(twi_daily.date,twi_daily.twi_num);plt.show()
