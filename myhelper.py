import tweepy
import pandas as pd
import numpy as np
import time
import datetime
import os
os.chdir(os.getcwd()+'\\Twitter-Analysis-With-Earning-Event')

def api_load():
    
    TOKEN = pd.read_csv("TOKEN.txt",sep=" ").columns.values
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
        print("Failed to access Twitter API!")
        return 0

def countdown(t):
    print("Rate limit exceed! wait for another 16min...if you believe this is abnormal, check code")
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1