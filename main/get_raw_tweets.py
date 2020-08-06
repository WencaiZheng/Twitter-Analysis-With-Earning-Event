import time
import os
import datetime
import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import processor._load_api as load_api
import processor._count_down as count_down
import processor._senti_process as senti_process

#global variable for the module
today_date = datetime.date.today()


class RawTweet:
    '''
    # PARAMETERS     
    # the dates I want to get, below says 7 days look back from today
    # key_word = ['$NKE'] ,tickers like this
    # most_recent_days = 7 # max is 8 for standard twitter api account
    # user_language = "en"# "zh-cn","en"
    '''
    def __init__(self,recent_days,user_language='en'):

        self.most_recent_days = recent_days # max is  8 for standard account
        self.user_language = user_language
        self.api = load_api.TwitterAPI.api_load()

    # idate is the until date of search
    def get_oneday_twitter(self,idate:str,key_word:str):
        # first max_id = None
        last_min_id = None
        result_full_df =pd.DataFrame()
        result_1qst = 0
        # 15 min get 180 requests at most
        i = 0
        while True:
            i += 1
            print("Processing request {0}".format(i))
            if i>5e3:print("Reach limit of 5000 requests, check it");break
            records=[]
            #twitters that are created at the actual date, idate is only search date, there is 1 day difference
            actual_date = str((pd.to_datetime(idate) - datetime.timedelta(days = 1)).date())
            # get a request
            try:
                result_1qst = self.api.search(q=key_word,until=idate,count=100,result_type="recent",
                    max_id=last_min_id,lang=self.user_language,tweet_mode="extended")
                        
                if len(result_1qst) == 0:
                    if i==1:
                        print("No result found! Check the date or keyword you search")
                    else:
                        print("All data collected")
                    break
                # concat this request to the last one
                records = [[x.id,x.created_at,x.user.id,x.user.screen_name,x.user.followers_count,x.full_text] for x in result_1qst]
                records_df = pd.DataFrame(records)
                records_df.columns = ["ID","Created","User_id","User_name","User_flr","Text"]
                # iterate the max id, one time smaller than last time
                last_min_id = result_1qst[-1].id-1
                print(last_min_id)
                # add one request to this 15 min result
                result_full_df= pd.concat([result_full_df,records_df],axis=0)

                if int(actual_date[-2:])!= result_1qst[-1].created_at.day:# if dates diff
                    print("Enough for the date {0}".format(actual_date))
                    result_full_df = result_full_df[result_full_df.Created.dt.day==int(actual_date[-2:])]
                    break

            except tweepy.error.RateLimitError as rle:
                print('the api reaches limit, change to a new one')
                self.api = load_api.TwitterAPI.change_api()
                
                try:
                    load_api.TwitterAPI.api_test()
                    #go to the next new request
                    continue
                # if change api does not work, just wait
                except tweepy.error.RateLimitError:
                    print('all apis capacity are full, wait for 15min cool down')
                    #wait for 15 mins
                    count_down.countdown(15)
                    continue
            except:
                print('something goes wrong.')

        #print info
        print("{0} requests have been finished for date {1} with {2}".format(i,actual_date,key_word))

        return result_full_df

    def get_multiple_dates(self,key_words):
        datelist = list(map(lambda x:str(x.date()),pd.date_range(end = today_date, periods=self.most_recent_days)))[::-1]
        #or you have specific datelist = ["2019-12-30"]
        for k in key_words:
            # all_results = dict()
            for idate in datelist:# add 15 min result to all
                print("Retrieving data for {0} at {1}".format(k,idate))
                # The date begins at earliest date
                search_date = str((pd.to_datetime(idate) + datetime.timedelta(days = 1)).date())
                idate_res = self.get_oneday_twitter(search_date,k)
                #all_results[idate] = idate_res
                #write one day before because of twitter setting
                tic_path = f'data\\raw_twitters\\{k}'
                # if path not exit, create folders
                if not os.path.exists(tic_path):os.makedirs(tic_path)
                idate_res.to_csv(f'{tic_path}\\{k}_{idate}.csv')

    
    def get_from_press(self,savename):

        save_path = 'data\\news\\' 
        period = self.most_recent_days
        request_counter = 0
        names = pd.read_csv('dictionary\\PressName.csv').iloc[:,-1].values
        result = []

        for iname in names:
            last_maxid = None
            time_gap = -1
            
            while time_gap < period:

                request_counter += 1
                time_line = self.api.user_timeline(iname,max_id=last_maxid,tweet_mode="extended")
                time_gap = (today_date - time_line[-1].created_at.date()).days
                if len(time_line) == 0:
                    time_gap = period+1
                    continue
                
                last_maxid = time_line[-1].id
                result += [[x.id,x.created_at,x.user.id,x.user.screen_name,x.user.followers_count,x.full_text] for x in time_line]
                
                print(request_counter,iname,time_line[-1].created_at)
                
                # reach limit
                if request_counter >= 899:
                    count_down.countdown(16)
                    request_counter = 0

        result_df = pd.DataFrame(result)
        result_df.columns = ["ID","Created","User_id","User_name","User_flr","Text"]
        # if path not exit, create folders
        if not os.path.exists(save_path):os.makedirs(save_path)
        result_df.to_csv(f'{save_path}\\{savename}.csv')


if __name__ == "__main__":
    # standard api limit, 7days max
    ####################################

    key_words = ['$RAD']
    recent_days = 7
    # get raw tweets and save them
    RawTweet(recent_days).get_multiple_dates(key_words)
    pass