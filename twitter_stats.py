import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import senti_ploter
from datetime import timedelta


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

    print(daily_senti)
    #plt.show()


def observe_annoucement(ticker,all_sentiments):

    earning_release = senti_ploter.get_earning_within(ticker,all_sentiments).index[0]

    pre_earn = all_sentiments[all_sentiments.index<earning_release]
    at_earn = all_sentiments[all_sentiments.index==earning_release]
    post_earn = all_sentiments[all_sentiments.index>earning_release]

    daily_pre = daily_tweets(pre_earn)
    daily_at =  daily_tweets(at_earn)
    daily_post =  daily_tweets(post_earn)

    daily_pre1 =  daily_pre[daily_pre.index != daily_at.index[0]]
    daily_at1 = daily_pre[daily_pre.index == daily_at.index[0]]
    daily_at0 = daily_at.copy()
    daily_at2 = daily_post[daily_post.index == daily_at.index[0]]
    daily_post1 = daily_post[daily_post.index != daily_at.index[0]]

    y1 = sum(daily_pre1.Avg_senti)/len(daily_pre1)
    y2 = sum(daily_at1.Avg_senti)/len(daily_at1)
    y3 = sum(daily_at0.Avg_senti)/len(daily_at0)
    y4 = sum(daily_at2.Avg_senti)/len(daily_at2)
    y5 = sum(daily_post1.Avg_senti)/len(daily_post1)

    y_pd = pd.DataFrame([y1,y2,y3,y4,y5]).T
    y_pd.columns = ["predate","pretime","attime","posttime","postdate"]
    print(y_pd)



    # whole_list = daily_pre.Avg_senti.to_list()+daily_at.Avg_senti.to_list()+daily_post.Avg_senti.to_list()
    # whole_list_idx = list(range(-len(daily_pre),0)) + [0] + list(range(1,len(daily_post)+1))
    
    # plt.title("Observe the annoucement one-hour sentiment change")
    # plt.plot(whole_list_idx,whole_list)
    # plt.show()


