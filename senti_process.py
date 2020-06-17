
import pandas as pd
import numpy as np
import os
import myfilter

class SentiProcess:
    def __init__(self,key_w,pos,neg):
        self.key_word = key_w
        self.pos_dic = pos
        self.neg_dic = neg
    
    def spliter(self,txt):
        spliter = self.key_word.upper()
        txt = spliter+txt.upper().split(spliter)[-1].split("$")[0]
        return txt
    

    def effective_ttr(self,xfile,thd):
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
        x_effc["fText"] = list(map(self.spliter,x_effc.Text))
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
    
    def senti_count(self,e_file,log_flag):
        """count how many positive or negative in a file named e_file
            log_flag: whether or not scale the count into log
        """
        if len(e_file)==0:
            print("file is empty")
            return None
        
        sentis = list(map(lambda x:self.get_senti(x,self.pos_dic,self.neg_dic),e_file.fText))
        e_file["Sentiment"] = sentis
        # one hot encoding
        sentis_df = pd.get_dummies(sentis)
        temp=pd.DataFrame([[0]*3]*len(sentis_df),columns=[-1,0,1])
        sentis_df = (temp+sentis_df).fillna(0)
        sentis_df.columns=["Negative","Unknown","Positive"]
        # s_file gives each ttr sentiment
        s_file = e_file.join(sentis_df)
        # change time zone from utc to est
        s_file["EST"] = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in s_file.Datetime]
        s_file.index = list(map(lambda x:x.replace(tzinfo=None),s_file["EST"]))
        # add all sentis get a count 
        s_file["All_counts"] = [1]*len(s_file)
        # count the hourly negative or positive ttr 
        partly_count = s_file.groupby(by="Hour").sum().loc[:,["Negative","Positive","All_counts"]]
        #scale it
        if log_flag:partly_count = np.log(partly_count+1)
        x_zero = pd.Series(24*[0])
        # fill the non-data zone as nan
        hour_count = pd.concat([partly_count,x_zero],axis=1).fillna(0).drop(columns=[0])
        # show negative times in nagative
        hour_count.Negative = -hour_count.Negative
        # save negative or positive tweets v5/5/20:
        save_file = s_file.loc[:,["User_name","Text","Sentiment","User_flr",]]
        pos_tweets = save_file[save_file.Sentiment==1]
        neg_tweets = save_file[save_file.Sentiment==-1]
        # standard  datetime
        idate = e_file.Created[0][:11]
        hour_count.index = list(map(lambda x:pd.to_datetime(f'{idate}{x}:00:00'),hour_count.index))
        return hour_count,pos_tweets,neg_tweets

    
    def get_all_senti(self,files,thres,is_log,is_save_senti):
        key_word = self.key_word
        #make other functions use these variables
        dates = [i[-14:-4] for i in files]
        # count sentiments 
        all_sentis,all_pos,all_neg = pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
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
            isenti,pos_tweets,neg_tweets = self.senti_count(e_file,is_log)
            # add today's senti to all
            all_sentis = pd.concat([all_sentis,isenti])
            # save the divided files if necessary

            senti_path = f'results\\{key_word}'
            if not os.path.exists(senti_path):os.makedirs(senti_path)
            all_pos = pd.concat([all_pos,pos_tweets],axis=0,sort=False)
            all_neg = pd.concat([all_neg,neg_tweets],axis=0,sort=False)

        if is_save_senti ==1:
            all_pos.to_csv(f'{senti_path}\\{key_word}_pos.csv')
            all_neg.to_csv(f'{senti_path}\\{key_word}_neg.csv')
            print("sentiment files are saved successfully")

        all_sentis = all_sentis.replace([np.inf,-np.inf],[np.nan,np.nan])
        # convert all_sentis from UTC time to EST time
        all_sentis["EST"] = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in all_sentis.index]
        all_sentis.index = list(map(lambda x:x.replace(tzinfo=None),all_sentis["EST"]))
        if len(all_sentis)==0:return []
        # add net sentiment
        all_sentis["NetSentiment"] = all_sentis.Positive + all_sentis.Negative
        return all_sentis