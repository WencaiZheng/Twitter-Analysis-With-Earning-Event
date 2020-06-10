import pandas as pd
import numpy as np
import os

def daily_tweets(files):
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