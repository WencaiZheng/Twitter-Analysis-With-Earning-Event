import datetime
import pandas as pd
import numpy as np
import re
from glob import glob
import os
import earnings_scraper
import senti_ploter as myPloter
import top_words
import senti_process
os.chdir(os.getcwd()+"\\Twitter-Analysis-With-Earning-Event")

################################## parameters needed
key_word ="$COST" #"SBUX" #TTWO, "TGT","WMT",
ticker = 'COST'

save_senti_flag = 1 # if 1, it saves the sentiment text files by date and positivity 
is_show_top_words = 1 ; topn = 5000 # show the top words for key words
#
log_scale_flag= 0 # log-scale or not
influencer_threshold = 50 # define influencer with follower
is_earning_release = 1
is_show_stock_price = 0 # no stock processing would be much faster
#################################

def my_dict():
    LM_dic = pd.read_csv("dictionary\\LoughranMcDonald_MasterDictionary_2018.csv")
    pos_dic = LM_dic[LM_dic.Positive!=0].Word.values
    neg_dic = LM_dic[LM_dic.Negative!=0].Word.values
    return pos_dic,neg_dic

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
    pos_dic,neg_dic = my_dict()
    # get all sentiment from all files, each file represent a day
    all_sentiments  = senti_process.get_all_senti(key_word,files,pos_dic,neg_dic,influencer_threshold,log_scale_flag,save_senti_flag)
    ###########################################################
    top_words.show_top(result_path,key_word,topn,is_show_top_words)
    #plot #####################################################
    myPloter.plotit(key_word,ticker,all_sentiments,is_show_stock_price,is_earning_release)