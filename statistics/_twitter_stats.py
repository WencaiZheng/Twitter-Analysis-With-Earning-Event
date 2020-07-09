import os
import re
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from collections import Counter
from glob import glob

import visualization._senti_ploter as senti_ploter


def calculate_top_words(result_path,topn):
    """ get top word
    """
    stopword = pd.read_csv("dictionary\\twitter_stopwords.txt",index_col=0).iloc[:,0].values
    pos_files=glob(result_path+"*pos*")
    neg_files=glob(result_path+"*neg*")
    pos_words,neg_words = "",""

    for i in range(len(pos_files)):
        ipos = pd.read_csv(pos_files[i])
        pos_words+= ipos.Text.sum().upper()

    for i in range(len(neg_files)):
        ineg = pd.read_csv(neg_files[i])
        neg_words+= ineg.Text.sum().upper()
            

    pos_dic = Counter(re.split('[^a-zA-Z]+', pos_words))
    neg_dic = Counter(re.split('[^a-zA-Z]+', neg_words))

    for w in pos_dic.keys():
        if w in stopword:
            pos_dic[w] = -1

    for w in pos_dic.keys():
        if w in stopword:
            neg_dic[w] = -1

    
    pos_df = pd.DataFrame(pos_dic.most_common())
    neg_df = pd.DataFrame(neg_dic.most_common())

    word_df = pd.concat([pos_df,neg_df],axis=1,join="outer")
    word_df.columns = ["positive_word","positive_count","negative_word","negative_count"]

    return word_df

def show_top(result_path,key_word,topn,show_flag):
    top_word = calculate_top_words(result_path,topn)
    top_word.to_csv(f'{result_path}{key_word}_topwords.csv')
    if show_flag:print(top_word.iloc[:topn,:])


def daily_tweets_all(files):
    """show some important statistics
    """
    stats= []
    dates = [i[-14:-4] for i in files] #get dates
    for i in range(len(dates)):
        idate = dates[i]
        ifile = files[i]
        xfile=pd.read_csv(ifile)
        if len(xfile) != 0:
            stats.append((idate,len(xfile),len(xfile.User_id.unique())))
        else:
            stats.append((idate,0,0))
    stats_pd = pd.DataFrame(stats,columns=["date","twi_num","uniq_user"])
    return stats_pd

def daily_tweets(all_sentiments):
    all_sentiments["date"]=all_sentiments.index.date
    daily_senti = all_sentiments.groupby('date').sum()
    daily_senti["Avg_senti"] = daily_senti.NetSentiment/daily_senti.All_counts*100
    return daily_senti


def daily_plot(daily_senti):
    senti_a = daily_senti.Avg_senti.values
    senti_v = daily_senti.All_counts.values
    x = daily_senti.index

    _, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.bar(x, senti_v, )
    ax2.plot(x, senti_a,'r-')

    ax1.set_xlabel('date',fontsize=20)
    ax2.set_ylabel('net sentiment/daily tweets (%)', color='r',fontsize=20)
    ax1.set_ylabel('daily tweets number', color='b',fontsize=20)

    
    #plt.show()


def observe_annoucement(ticker,all_sentiments):

    earning_release = senti_ploter.TwitterPlot.get_earning_within(ticker,all_sentiments).index[0]

    pre_earn = all_sentiments[all_sentiments.index<earning_release]
    at_earn = all_sentiments[all_sentiments.index==earning_release]
    post_earn = all_sentiments[all_sentiments.index>earning_release]

    daily_pre = daily_tweets(pre_earn)
    daily_at =  daily_tweets(at_earn)
    daily_post =  daily_tweets(post_earn)

    release_date = earning_release.date()

    daily_pre1 =  daily_pre[daily_pre.index != release_date].fillna(0)
    daily_at1 = daily_pre[daily_pre.index == release_date].fillna(0)
    daily_at0 = daily_at.copy().fillna(0)
    daily_at2 = daily_post[daily_post.index == release_date].fillna(0)
    daily_post1 = daily_post[daily_post.index != release_date].fillna(0)

    data_stack = [daily_pre1,daily_at1,daily_at0,daily_at2,daily_post1]

    temp_y = [0 if sum(x.All_counts) ==0 else sum(x.Avg_senti)/sum(x.All_counts) for x in data_stack]
    y_pd = pd.DataFrame(temp_y).T
    y_pd.columns = ["predate","pretime","attime","posttime","postdate"]
    print(y_pd)

def pre_opening_analysis(keyword_list,flr_thres):
    for key_word in keyword_list:
        file_name = f'data\\senti_results\\{key_word}\\{key_word}_{flr_thres}.csv'
        result = pd.read_csv(file_name,index_col=0)
        result['user_score'] = result.User_flr * result.Sentiment
        result.index = pd.to_datetime(result.index)
        since_when =  pd.to_datetime(result.index[-1] - timedelta(days=1))
        result = result[result.index > since_when]
        aggregated_result = result.loc[:,['Sentiment','user_score']].resample('5T').sum()
        senti_ploter.TwitterPlot(key_word).plot_preopen_senti(aggregated_result)
    

if __name__ == "__main__":
    
    print(re.split('[^a-zA-Z]+', "s $ss 12 @@ x"))