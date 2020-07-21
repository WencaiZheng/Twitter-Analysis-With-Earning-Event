import tweepy
import pandas as pd
import numpy as np
import time
import datetime
import os
#change it to the address where the file is located in your computer
#os.chdir('C:\\Users\\wenca\\Desktop\\GitRepo\\Twitter-Analysis-With-Earning-Event\\')

def api_load():
    
    TOKEN = pd.read_csv("TOKENS\\TOKEN.txt",sep=" ").columns.values
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

