import time
import os
import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta,date

import processor._load_api as load_api
import processor._count_down as count_down
import processor._senti_process as senti_process
import processor._automail as automail
import main.analysis_main as analysis
import news._news_sa as news_sa
import main.get_raw_tweets as grt
import visualization._plotly_ploter as myplot
import processor._load_intraday as load_intraday



nowdate= str(date.today())

save_dir = 'data\\raw_twitters'
trend_dir = 'data\\twitter_trend'

class RealTimeTweet:
    '''
    Update real time tweets number alert for list of tickers
    every half hour
    '''
    # class variable api
    api = load_api.TwitterAPI.api_load()
    # the sp500 names we want to moiniter
    #names = pd.read_csv('dictionary\\SP500.csv').Symbol.values
    # the request has limit, it should not exceed 180/15min
    request_counter = 0
    #



    def __init__(self):
        #nothing here
        pass

    # idate is the until date of search
    @classmethod
    def one_ticker(cls,key_word):
        # time gap is half hour
        period = 0.5
        # the first request
        
        last_maxid = None
        time_gap = -1

        result = []
        while time_gap < period:
            #within half hour period tweets this collected one ticker
            
            try:
                # get tweets with search request
                result_1qst = cls.api.search(q=key_word,count=100,result_type="recent",
                        max_id=last_maxid,lang='en',tweet_mode="extended")

            except tweepy.error.RateLimitError:

                print('the api reaches limit, change to a new one')
                cls.api = load_api.TwitterAPI.change_api()
                
                try:
                    load_api.TwitterAPI.api_test()
                    #go to the next new request
                    continue
                # if change api does not work, just wait
                except tweepy.error.RateLimitError:
                    print('all apis are full, wait for 15min cool down')
                    #wait for 15 mins
                    count_down.countdown(15)
                    continue
            
            # request success
            cls.request_counter += 1
            
            # boundary condition
            if len(result_1qst) == 0:
                print("No result found! Check the date or keyword you search")
                records_df = pd.DataFrame(columns = ["ID","Created","User_id","User_name","User_flr","Text"])
                break
            
            #change from utc to est
            esttime = pd.to_datetime(result_1qst[-1].created_at)-timedelta(hours=4)
            # get the final tweets and the current time's time gap, second to hour
            time_gap = (cls.nowtime - esttime).total_seconds()/3600
            last_maxid = result_1qst[-1].id
            result += [[x.id,x.created_at,x.user.id,x.user.screen_name,x.user.followers_count,x.full_text] for x in result_1qst]
            print(cls.request_counter,key_word,esttime)
            
                    
            # concat this request to the last one
            records_df = pd.DataFrame(result)
            records_df.columns = ["ID","Created","User_id","User_name","User_flr","Text"]
        
        # change from UCT to EST time zone
        records_df.index = pd.to_datetime(records_df.Created)
        records_df = senti_process.SentiProcess._utc_to_est(records_df)
        
        # Most updated one is at the bottom
        records_df = records_df.sort_index(ascending=True)
        return records_df
    
    @classmethod
    def load_file(cls,kw):
        #load file of the specific ticker
        tic_path = f'{save_dir}\\{kw}'
        if not os.path.exists(tic_path):
            os.makedirs(tic_path)
        try:
            existed_file = pd.read_csv(f'{tic_path}\\{kw}_{nowdate}.csv',index_col=0)
        except FileNotFoundError:
            existed_file = pd.DataFrame(columns = ["ID","Created","User_id","User_name","User_flr","Text"])
        # change index form string to datatimeindex
        existed_file.index = pd.to_datetime(existed_file.index)
        # The most updated is at the bottom
        existed_file =  existed_file.sort_index(ascending=True)
        return existed_file
    

    @staticmethod
    def _judge(past,new):
        # The condition is that the new is larger than 1.5 times of the past average tweets
        # It is a simple condition, let's see
        # if the past average is zero, it just return 0
        if past == 0 or new < 20:
            return 0
        return new >= past * 1.8     


    @classmethod
    def intrigue_warning(cls,kw,past,new):
        """It add statistic data to the email body
        """
        cls.email_body += f'For {kw}, historical volume: {past}, '+\
            f'historical positve/negatives score: {cls.exist_pos}/{cls.exist_neg}. '+\
            f'New half hour volume: {new}, '+\
            f'positve/negatives score: {cls.new_pos}/{cls.new_neg}.\n\n'

        pass

    @classmethod
    def get_senti(cls,kw,one_df):
        """get the sentiment percentage for a period of time
        """
        senti_obj = senti_process.SentiProcess(kw)
        e_one_df = senti_obj.effective_ttr(one_df,5)
        isenti_hourly,itweets = senti_obj.senti_count(e_one_df,log_flag=0)
        pos_score = sum(itweets[itweets.Sentiment>0].Sentiment)/len(one_df)*100
        neg_score = sum(itweets[itweets.Sentiment<0].Sentiment)/len(one_df)*100
        return np.round(pos_score,2),np.round(neg_score,2)

    @classmethod
    def moniter_all(cls,names_):
        # the names in the monitor pool
        cls.names = names_
        cls.today_trend = pd.DataFrame(columns = names_)
        #everytime empty the email body
        cls.email_body = ""
        # initialize the counter
        cls.request_counter = 0
        # only get now's hour and minute
        cls.nowtime = datetime.now()
        nowtimestr = str(cls.nowtime)[:16]
        # creat a array of 0 and 1 to tell if any ticker has high trend
        now_trend = pd.DataFrame([0]*len(cls.names),index =cls.names,columns=[nowtimestr]).T
        """['$'+x for x in cls.names]
        """
        keyword_list = [x for x in cls.names]
        for kw in keyword_list:
            existed_df = cls.load_file(kw)
            one_df = cls.one_ticker(kw)
            if len(one_df)==0:continue

            # concat the one hour df and the exited file
            concated_df = pd.concat([existed_df,one_df],axis=0).drop_duplicates()
            
            # Only get past half hour tweets, one half hour before tweets are the existed tweets
            one_df = concated_df[concated_df.index > cls.nowtime-timedelta(minutes=30)]
            existed_df = concated_df[concated_df.index < cls.nowtime-timedelta(minutes=30)]
           
            # calculate the average half-hourly existed file
            existed_hourly = existed_df.loc[:,'User_flr'].resample('30T').sum()
            try:
                # calculate the overall tweets volume over the hours it covers
                past_avg = np.around(len(existed_df) / sum(existed_hourly.values != 0),0)
            except:
                past_avg = 0
            # the past hour twitter volume
            new_count = np.around(len(one_df),2)
            # compare the curretnly twitter number is rising or not

            if RealTimeTweet._judge(past_avg,new_count):

                # get sentiment of the trending tickers,set them as the class variables
                cls.new_pos,cls.new_neg = cls.get_senti(kw,one_df)
                cls.exist_pos,cls.exist_neg = cls.get_senti(kw,existed_df)
                # get the earning to the email body
                RealTimeTweet.intrigue_warning(kw,past_avg,new_count)
                # exceed the past average
                """now_trend.loc[nowtimestr,kw[1:]] = 1
                """
                # here we only want to use ticker name, which is AAPL instead of $AAPL
                now_trend.loc[nowtimestr,kw[:]] = 1
           
            #save the new file as the concated file as raw tweets
            concated_df.to_csv(f'{save_dir}\\{kw}\\{kw}_{nowdate}.csv')

        # analyze the trend tickers
        cls.analyze_trend(now_trend)
        
        return now_trend
    
    @classmethod
    def analyze_trend(cls,now_trend):
        #analyze the tickers
        trendup_ticker = now_trend.columns[now_trend.iloc[-1,:].values == 1]
        print(f'There are {[i for i in trendup_ticker]} trending right now')
        
        try:
            existed_trend = pd.read_csv(f'{trend_dir}\\{nowdate}.csv')
        except FileNotFoundError:
            existed_trend = pd.DataFrame(columns = cls.names)
        # add the new status in the file
        # see if the new hourly volume exceed the past average volume 1 or 0
        trend_df  =  pd.concat([existed_trend,now_trend],axis=0,join='outer',sort=True)
        trend_df.to_csv(f'{trend_dir}\\{nowdate}.csv')
        # send email to target
        cls.send_email(trendup_ticker)
        pass
    

    @classmethod
    def realtime_macro(cls,macro_type_,recentday):
        #initialize the email body
        cls.email_body= ""
        # this macro type is from FX, Brexit, or Stimulus
        filename = macro_type_
        grt.RawTweet(recent_days=recentday).get_from_accounts('MacroAccounts', savename = filename)
        #load the saved file to rank the name
        top_names,top_tweets = analysis.analysis_macro(filename)
        #
        names = top_names[top_names!=0].index
        print(names)
        for i in names:
            if top_names.loc[i] <= 3:
                print(f'Not enough tweets related, only {top_names.loc[i]}.')
                return 0
            cls.email_body += f'\n\n\nThere are {top_names.loc[i]} tweet(s) about {i} and they are:\n\n'+'\n'.join(top_tweets[i])
        #send the email
        cls.send_email(names)
    #

    @classmethod
    def analysis_topics(cls,recentday):
        #initialize the email body
        cls.email_body= ""
        # this macro type is from FX, Brexit, or Stimulus
        filename = 'all_topics'
        grt.RawTweet(recent_days=recentday).get_from_accounts('MacroAccounts', savename = filename)
        #load the saved file to rank the name
        top_topic = analysis.analysis_topics(filename)
        # it counts how many times it is mentioned in half hour
        top_num = pd.get_dummies(top_topic.TOPIC, prefix='TOPIC')
        # get half hour tweet count
        new_half = top_num.resample('1H').sum()
        print(top_num.columns)
        # merge with EXISTED form
        existed = pd.read_csv('data\\macro\\TopicCounts.csv',index_col=0)
        existed.index = pd.to_datetime(existed.index)
        new_file = pd.concat([existed,new_half],axis=0).fillna(0)
        #drop duplicates
        new_file = new_file[~new_file.index.duplicated(keep='last')]
        #save file
        new_file.to_csv('data\\macro\\TopicCounts.csv')
        # whether to alert
        send_name = []
        # stock price qqq and iwm
        price1 = load_intraday.get_hourly_ratio('QQQ')
        price2 = load_intraday.get_hourly_ratio('IWM') 
        price = pd.concat([price1,price2],axis=1).dropna()
        pricer = price.iloc[:,0]/price.iloc[:,1]
        for i in new_file.columns:
            # get this topic
            itop = new_file[i]
            # if trend is there: new tweet number are above the 75% persentile
            # if 1==1 or (itop.iloc[-1]+itop.iloc[-2] >= itop.quantile(0.75) and itop.iloc[-1]+itop.iloc[-2]>5) :
            if i == 'TOPIC_VACCINE' or i == 'TOPIC_COVID' or i == 'TOPIC_LOCKDOWN':
                myplot.TwitterPlot.plot_topicswprice(i,itop,pricer)
                #
                send_name.append(i)
            else:
                print(f'Not enough tweets related {i}, only {itop.iloc[-1]+itop.iloc[-2]}.')
        #send the email
        #cls.send_email(send_name)
    #
    @classmethod
    def send_email(cls,trendup_ticker):
        #send to some one
        toaddr = ['rangerrod1@gmail.com','wz1298@nyu.edu']#

        if len(trendup_ticker)==0:
            # don't send email
            summary = f'There is no ticker/topic(s) in the past half hour trending up.\n'
            # dont send email if there's nothing happened
            print(summary)
        else:
            summary = f'There are following ticker/topic(s) trending right now: {" ".join(trendup_ticker)}. '\
                f'Detailed information:\n \n '
            #
            cls.email_body = summary + cls.email_body
            #
            automail.SendEmail(toaddr).send_realtime_email(cls.email_body)

    @classmethod
    def run_main(cls,keyword_list):
        # timing for run the monitor function
        
        while True:
            now_min = datetime.now().minute
            if now_min == 0 or now_min==30:
                RealTimeTweet.moniter_all(keyword_list)
                count_down.countdown(2)

            elif now_min<30:
                count_down.countdown(30-now_min)
            
            elif now_min>30:
                count_down.countdown(60-now_min)
    
    @classmethod
    def run_macro(cls,macro_type_):
        # choose macro type, the type decides monitor keywords, it is file name
        # for example: Brexit or timulus, FX
        cls.macro_type = macro_type_
        while True:
            now_min = datetime.now().minute
            if now_min == 0:
                cls.realtime_macro(macro_type_,recentday=1/24)
                count_down.countdown(5)
            else:
                count_down.countdown(60-now_min)


if __name__ == "__main__":

    # run all tickers
    # keyword_list = news_sa.load_earning_names()
    RealTimeTweet.analysis_topics(recentday=1)
    #allf = RealTimeTweet.realtime_macro('Stimulus')
    #RealTimeTweet.run_macro()
    # RealTimeTweet.run_main()


    pass






zipcodes = range(10001,11201)
category = ['senior-care','memory-care-facilities']
for i in zipcodes:
    for j in category:
        url = f'https://www.caring.com/local/search?location={i}&sortBy=TOP_RATED&type={j}'
        getinfofromthis(url)