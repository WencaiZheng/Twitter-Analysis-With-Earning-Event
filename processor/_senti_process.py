import os
import re
import gensim
import nltk
import numpy as np
import pandas as pd
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.stem.porter import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import processor._fix_dictionary as mydictionary

nltk.download('wordnet')

sid_obj = SentimentIntensityAnalyzer() 
save_path = 'data\\senti_results\\'

#class
class SentiProcess:
    """
    The class process the raw tweets and define if one is positive or negative
    then it counts the hourly positive, negative and all tweets 
    it saved the results by the keyword it was searched from sraper_main
    """
    def __init__(self,key_w):
        self.key_word = key_w     
        # load the main dictionary
        self.pos_dic,self.neg_dic = mydictionary.TwitterDict.new_dict()
        # load the pre filter dictionary
        self.pre_dic,self.pre_neg =  mydictionary.TwitterDict.pre_dict()
 
    
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

    def get_senti(self,rawtxt):
        """for a sentence, it gives its sentiment
        """
        txt_list= rawtxt.split(" ")
        pos_count,neg_count =0,0
        for i in txt_list:
            if i in self.pos_dic:pos_count+=1
            if i in self.neg_dic:neg_count+=1
        # positive
        if pos_count>neg_count:senti = 1
        elif pos_count<neg_count:senti = -1
        else: senti = 0
        return senti
    
    def pre_filter(self,rawtxt):
        is_pos = sum([keyw in rawtxt for keyw in self.pre_dic])
        is_neg = sum([keyw in rawtxt for keyw in self.pre_neg])
        # if they are both zero or both not 0, which mean it is vague
        if not is_pos and not is_neg: return 0
        elif is_pos and is_neg:return 0
        # if one of them are zero one is not
        elif is_pos and not is_neg:return 1
        elif is_neg and not is_pos:return -1
        

    def senti_count(self,e_file,log_flag):
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
            pre_senti = self.pre_filter(x)
            # let presenti filter first, if zero, use vader
            if pre_senti == 0:
                vader_senti = sid_obj.polarity_scores(x)['compound']
                if vader_senti==0:
                    dict_senti = self.get_senti(x)
                    sentis.append(dict_senti)
                else:
                    sentis.append(vader_senti)
            # if pre filter sentiment result is not zero, use it directly
            else:
                sentis.append(pre_senti)

        #return the sentiment number of each tweet to tweet file
        e_file["Sentiment"] = sentis
        s_file = e_file.copy()
        s_file.index = s_file.Datetime

        # add all sentis get a count 
        s_file["All_counts"] = [1]*len(s_file)
        # count the hourly negative or positive ttr 
        hour_count = s_file.loc[:,['Sentiment','All_counts']].resample('1H').sum()
        #scale it
        if log_flag:hour_count = np.log(hour_count+1)
        # show positive or negative
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
        """There should be index instead of Created
        """
        ifile.index = pd.to_datetime(ifile.loc[:,'Created'])
        ifile["datehour"] = list(map(lambda x:f'{x.date()} {x.hour}',ifile.index))
        hourly_data =  ifile.groupby("datehour")['Text'].apply(lambda x: x.sum()).sort_index()
        # count news numbers
        count = np.zeros(len(hourly_data))
        for kw in kw_list:
            count += np.array(list(map(lambda x:x.upper().count(kw),hourly_data.values)))
        
        count_series = pd.Series(count,index=hourly_data.index.copy())
        all_sentis = count_series.fillna(0)
        # change from UTC time to EST
        all_sentis.index = pd.to_datetime(list(map(lambda x:x+':00:00',all_sentis.index)))

        return all_sentis
    
    @staticmethod
    def _utc_to_est(df):
        """It convert the index of dataframe from utc time zone to est time zone
        """
        df["EST"] = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in df.index]
        df.index = list(map(lambda x:x.replace(tzinfo=None),df["EST"]))
        df = df.drop(columns=['EST'])
        return df
    
    @staticmethod
    def _stemmer(text):
        '''
        get out all the stop words
        stem the word
        '''
        stemmer = PorterStemmer()
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS:
                stemmed = stemmer.stem(WordNetLemmatizer().lemmatize(token, pos='v'))
                result.append(stemmed)
        return result

    @staticmethod
    def _only_letter(text):
        '''
        get only letter, no punctuation
        '''
        return re.sub('[^a-zA-Z]+', ' ', text).split(' ')

    def get_all_senti(self,files,thres,is_log,is_save_senti):
        key_word = self.key_word
        #make other functions use these variables
        dates = [i[-14:-4] for i in files]
        # count sentiments 
        all_sentis,all_tweets = pd.DataFrame(),pd.DataFrame()
        for i in range(len(dates)):
            idate = dates[i]
            ifile = files[i]
            xfile=pd.read_csv(ifile,)
            # step 1 filter out all the unqualified ones, if empty return none
            e_file = self.effective_ttr(xfile,thres)
            # if empty, goes to next date file
            if len(e_file)==0:
                print("file is empty for {0}".format(idate))
                continue 
            # step 2
            isenti_hourly,itweets_single = self.senti_count(e_file,is_log)
            # add today's senti to all
            all_sentis = pd.concat([all_sentis,isenti_hourly])
            # all_tweets file is the file contains all individual tweets
            all_tweets = pd.concat([all_tweets,itweets_single],axis=0,sort=False)

        all_sentis = all_sentis.replace([np.inf,-np.inf],[np.nan,np.nan])
        # make the index the EST time instead of original twitter UCT time
        # all_sentis.index = pd.to_datetime(all_sentis.index)
        all_sentis = SentiProcess._utc_to_est(all_sentis)
        # if the file is empty, then raise exception
        if len(all_sentis)==0:
            raise Exception('There are not enough sentiments to show.')

        # save the files if necessary 'results/tickername/file.csv'
        if is_save_senti ==1:
            tic_path = f'{save_path}{key_word}\\'
            if not os.path.exists(tic_path):os.makedirs(tic_path)
            # transfer the time zone
            # make the index the EST time instead of original twitter UCT time
            # all_tweets.index = pd.to_datetime(all_tweets.index)
            all_tweets = SentiProcess._utc_to_est(all_tweets)
            all_tweets.to_csv(f'{tic_path}{key_word}_{thres}.csv')
            print("sentiment files are saved successfully")
        # all_sentis is the file that contains all HOURLY sentiment data
        return all_sentis

    
    def get_accountsinfo(self,files):
        """
        read the raw tweets return the accounts that are interested in this topic
        """
        key_word = self.key_word
        #make other functions use these variables
        dates = [i[-14:-4] for i in files]
        # count sentiments 
        all_sentis,all_tweets = pd.DataFrame(),pd.DataFrame()
        for i in range(len(dates)):
            idate = dates[i]
            ifile = files[i]
            xfile=pd.read_csv(ifile,)
            # step 1 filter out all the unqualified ones, if empty return none
            e_file = xfile.groupby('User_name').count().sort_values('User_flr',ascending=False)
            all_tweets = pd.concat([all_tweets,xfile],axis=0)
        #
        all_accounts = all_tweets.groupby('User_name').count().ID
        # add the followers info
        all_flr = all_tweets.groupby('User_name').sum().User_flr
        # if the file is empty, then raise exception
        all_info = pd.concat([all_accounts,all_flr],axis=1)
        # 
        all_info.columns = ['Freq','Score']
        all_info['Flr'] = all_info.Score/all_info.Freq
        #
        all_info.sort_values('Freq', ascending=False, inplace=True)
        if len(all_info)==0:
            raise Exception('There are not enough sentiments to show.')
        #
        return all_info