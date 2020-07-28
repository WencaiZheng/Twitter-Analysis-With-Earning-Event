import tweepy
import pandas as pd
import numpy as np
import time
import datetime
import os
#change it to the address where the file is located in your computer
#os.chdir('C:\\Users\\wenca\\Desktop\\GitRepo\\Twitter-Analysis-With-Earning-Event\\')
class TwitterAPI():
    """
    Load different apis to expand the tweets api limit
    default api is the first row
    """
    api_id = 0
    max_api = 3
    def __init__(self):
        pass

    @classmethod
    def api_load(cls):
        #load api
        TOKEN = pd.read_csv("TOKENS\\TOKEN.txt",sep=" ",header=None).iloc[cls.api_id,:]
        consumer_key, consumer_secret,access_token_key, access_token_secret = TOKEN
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        api = tweepy.API(auth)
        #Access to twitter successfully or not
        try:
            api.verify_credentials()
            print("Successfully access to Twitter API!")
            return api
        except:
            raise Exception("Failed to access Twitter API!")

    @classmethod
    def change_api(cls):
        #change another api to use if the previous one is full
        cls.api_id += 1
        #if the apis all used up, use the first one
        if cls.api_id >= cls.max_api:
            cls.api_id = 0
        return cls.api_load()

    @classmethod
    def api_test(cls):
        test_api =  cls.api_load()
        test_api.search(q='Test',count=100,result_type="recent",
                    max_id=None,lang='en',tweet_mode="extended")

        
