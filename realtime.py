import main.get_raw_tweets as grt
import main.analysis_main as analysis
import main.realtime_tweets as rtt

# import main.news_main as news_main
import processor._count_down as count_down
import news._news_sa as news_sa
import pandas as pd
import os
#change it to the address where the file is located in your computer
#os.chdir('C:\\Users\\wenca\\Desktop\\GitRepo\\Twitter-Analysis-With-Earning-Event\\')

def Function4():
    """real time update for the large twitter volume ticker
    """
    keyword_list = news_sa.load_earning_names()
    rtt.RealTimeTweet.run_main(keyword_list)

def Function5():
    """real time alert system for some macro indicators like FX
    """
    #save the tweets from the macro twitter accounts and save below
    rtt.RealTimeTweet.run_macro()
    
if __name__ == "__main__":
    

    Function5()

    pass



    

    
