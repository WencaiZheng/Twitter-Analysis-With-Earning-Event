import os
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sid_obj = SentimentIntensityAnalyzer() 
save_path = 'data\\senti_results\\'

#class
class SentiProcess:
    """
    The class process the raw tweets and define if one is positive or negative
    then it counts the hourly positive, negative and all tweets 
    it saved the results by the keyword it was searched from sraper_main
    """
    def __init__(self,key_w,pos,neg):
        self.key_word = key_w
        self.pos_dic = pos
        self.neg_dic = neg
    
    def spliter(self,txt):
        """
        Filter out the unrelated $tickers
        """
        spliter = self.key_word.upper()
        txt = spliter+txt.upper().split(spliter)[-1].split("$")[0]
        return txt
    

    def effective_ttr(self,xfile,thd):
        """
        Filter out the tweets that are effective by our definition
        """
        if len(xfile)==0:return []
        xfile["Datetime"] =pd.to_datetime(xfile.Created)
        xfile["Hour"] = xfile.Datetime.dt.hour
        xfile=xfile.sort_values(by="Datetime")
        # filter the effective user twitter
        is_effec = xfile.User_flr>=thd #using follower number to filter
        # use frequency twitter
        # is_effec = list(map(myfilter.Filter.freq_filter,xfile.User_id))
        x_effc = xfile[is_effec]

        x_effc.index = range(len(x_effc))
        # split the $ sign and get only the key word
        x_effc["sText"] = list(map(self.spliter,x_effc.Text))
        return x_effc

    @staticmethod
    def get_senti(rawtxt,pos_dic,neg_dic):
        txt_list= rawtxt.split(" ")
        pos_count,neg_count =0,0
        for i in txt_list:
            if i in pos_dic:pos_count+=1
            if i in neg_dic:neg_count+=1
        # positive
        if pos_count>neg_count:senti = 1
        elif pos_count<neg_count:senti = -1
        else: senti = 0
        return senti
    
    def senti_count(self,idate,e_file,log_flag):
        """count how many positive or negative in a file named e_file
            log_flag: whether or not scale the count into log
        """
        if len(e_file)==0:
            print("file is empty")
            return None
        # initialize the sentiment list for each tweet
        sentis =  []
        for x in e_file.sText:
            #calculcate the compound score of each tweet first
            vader_senti = sid_obj.polarity_scores(x)['compound']
            dict_senti = self.get_senti(x,self.pos_dic,self.neg_dic)
            if vader_senti==0:
                sentis.append(dict_senti)
            else:
                sentis.append(vader_senti)
        #return the sentiment number of each tweet to tweet file
        e_file["Sentiment"] = sentis
        s_file = e_file.copy()
        s_file.index = s_file.Datetime
        # change time zone from utc to est
        # s_file["EST"] = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in s_file.Datetime]
        # s_file.index = list(map(lambda x:x.replace(tzinfo=None),s_file["EST"]))
        # add all sentis get a count 
        s_file["All_counts"] = [1]*len(s_file)
        # count the hourly negative or positive ttr 
        partly_count = s_file.loc[:,['Sentiment','All_counts']].resample('1H').sum()
        #scale it
        if log_flag:partly_count = np.log(partly_count+1)
        hour_count = partly_count.copy()
        # show negative times in nagative
        hour_count['Positive'] = hour_count[hour_count.Sentiment>0].Sentiment
        hour_count['Negative'] = hour_count[hour_count.Sentiment<0].Sentiment
        hour_count=hour_count.fillna(0)
        # save negative or positive tweets v5/5/20:
        save_file = s_file.loc[:,["Sentiment","User_flr","Text","User_name"]]
        return hour_count,save_file

    @staticmethod
    def analysis_news(kw_list,filename):
        save_path = 'data\\news\\'
        ifile = pd.read_csv(f'{save_path}{filename}.csv',index_col = 0)

        ifile.index = pd.to_datetime(ifile.loc[:,'Created'])
        ifile["datehour"] = list(map(lambda x:f'{x.date()} {x.hour}',ifile.index))
        hourly_data =  ifile.groupby("datehour")['Text'].apply(lambda x: x.sum()).sort_index()
        # count news numbers
        count = np.zeros(len(hourly_data))
        for kw in kw_list:
            count += np.array(list(map(lambda x:x.upper().count(kw),hourly_data.values)))
        
        count_series = pd.Series(count,index=hourly_data.index.copy())
        all_sentis = count_series.fillna(0)
        # change from UTC time to EDT
        all_sentis.index = pd.to_datetime(list(map(lambda x:x+':00:00',all_sentis.index)))
        temp = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in all_sentis.index]
        all_sentis.index = list(map(lambda x:x.replace(tzinfo=None),temp))
        return all_sentis
    
    @staticmethod
    def _utc_to_est(df):
        """It convert the index of dataframe from utc time zone to est time zone
        """
        df["EST"] = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in df.index]
        df.index = list(map(lambda x:x.replace(tzinfo=None),df["EST"]))
        return df

    def get_all_senti(self,files,thres,is_log,is_save_senti):
        key_word = self.key_word
        #make other functions use these variables
        dates = [i[-14:-4] for i in files]
        # count sentiments 
        all_sentis,all_tweets = pd.DataFrame(),pd.DataFrame()
        for i in range(len(dates)):
            idate = dates[i]
            ifile = files[i]
            xfile=pd.read_csv(ifile)
            # step 1 filter out all the unqualified ones, if empty return none
            e_file = self.effective_ttr(xfile,thres)
            # if empty, goes to next date file
            if len(e_file)==0:
                print("file is empty for {0}".format(idate))
                continue 
            # step 2
            isenti_hourly,itweets_single = self.senti_count(idate,e_file,is_log)
            # add today's senti to all
            all_sentis = pd.concat([all_sentis,isenti_hourly])
            # all_tweets file is the file contains all individual tweets
            all_tweets = pd.concat([all_tweets,itweets_single],axis=0,sort=False)

        all_sentis = all_sentis.replace([np.inf,-np.inf],[np.nan,np.nan])
        # convert all_sentis from UTC time to EST time
        all_sentis = SentiProcess._utc_to_est(all_sentis)
        # if the file is empty, then raise exception
        if len(all_sentis)==0:
            raise Exception('There are not enough sentiments to show.')

        # save the files if necessary 'results/tickername/file.csv'
        if is_save_senti ==1:
            tic_path = f'{save_path}{key_word}\\'
            if not os.path.exists(tic_path):os.makedirs(tic_path)
            # transfer the time zone
            all_df = SentiProcess._utc_to_est(all_tweets.sort_index())
            all_df.to_csv(f'{tic_path}{key_word}_{thres}.csv')
            print("sentiment files are saved successfully")
        # all_sentis is the file that contains all HOURLY sentiment data
        return all_sentis