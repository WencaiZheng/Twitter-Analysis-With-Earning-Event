import main.get_raw_tweets as grt
import main.analysis_main as analysis
import main.realtime_tweets as rtt

# import main.news_main as news_main
import news._news_sa as news_sa
import pandas as pd
import os
#change it to the address where the file is located in your computer
#os.chdir('C:\\Users\\wenca\\Desktop\\GitRepo\\Twitter-Analysis-With-Earning-Event\\')

def Function1():
    """ Function 3: get ticker names having earnings next few days
    """
    news_sa.save_earning_names(recent_day = 5,index_code = "SP5") # next 5 days RU3000/SP500 list name

def Function2():
    """real time update for the large twitter volume ticker
    """
    keyword_list = news_sa.load_earning_names()
    rtt.RealTimeTweet.run_main(keyword_list)
    



if __name__ == "__main__":
    
    #Function1()
    Function2()


    pass



    

    
