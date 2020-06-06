import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import datetime
import os
today_date = datetime.date.today()
os.chdir(os.getcwd()+"\\Twitter-Analysis-With-Earning-Event")

############               PARAMETERS             ###################
# the dates I want to get, below says 7 days look back from today
key_word = ["$RH"] #"SFIX","AVGO","HD","GOOG","SBUX""NBL","NVDA","INTC","AMD","TSM","TGT","WMT",EXPE","TJX","HRL","NVDA","BBY",
most_recent_days = 3 # max is  8 for standard account
user_language = "en"# "zh-cn","en"
#####################################################################





# twitter api
TOKEN = pd.read_csv("TOKEN.txt",sep=" ").columns.values
consumer_key, consumer_secret,access_token_key, access_token_secret=TOKEN
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)
#Access to twitter successfully or not
try:api.verify_credentials();print("Successfully access to Twitter API!")
except:print("Failed to access Twitter API!")

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

# idate is the until date of search
def get_oneday_twitter(idate:str,key_word:str,max_rqst:int):
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
            result_1qst = api.search(q=key_word,until=idate,count=100,result_type="recent",
                max_id=last_min_id,lang=user_language,tweet_mode="extended")
                    #transform into dataframe
            if len(result_1qst) == 0:
                if i==1:
                    print("No result found! Check the date or keyword you search")
                else:
                    print("All data collected")
                break


            # concat this request to the last one
            [records.append([x.id,x.created_at,x.user.id,x.user.screen_name,x.user.followers_count,x.full_text]) for x in result_1qst]
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


        except:
            print("Rate limit exceed! wait for another 16min...if you believe this is abnormal, check code")
            countdown(16*60)
            
    print("{0} requests have been finished for date {1} with {2}".format(i,actual_date,key_word))
    result_full_df.index= range(len(result_full_df))# Rearrange index

    return result_full_df

if __name__ == "__main__":
    # standard api limit, 7days max
    ####################################
    datelist = list(map(lambda x:str(x.date()),pd.date_range(end = today_date, periods=most_recent_days)))[::-1]
    #or you have specific datelist = ["2019-12-30"]
    for k in key_word:
        all_results = dict()
        for ith,idate in enumerate(datelist):# add 15 min result to all
            print("Parsing data for {0} at {1}".format(k,idate))
            # The date begins at earliest date
            search_date = str((pd.to_datetime(idate) + datetime.timedelta(days = 1)).date())
            idate_res = get_oneday_twitter(search_date,k,max_rqst=178)
            #all_results[idate] = idate_res
            #write one day before because of twitter setting
            tic_path = "twitters\\{0}".format(k)
            # if path not exit, create folders
            if not os.path.exists(tic_path):os.makedirs(tic_path)
            idate_res.to_csv(tic_path+"\\{0}_{1}.csv".format(k,idate))