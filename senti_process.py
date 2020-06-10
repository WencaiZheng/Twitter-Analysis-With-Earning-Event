
import pandas as pd
import numpy as np
import os

class SentiProcess:
    def __init__(self,key_w,pos,neg):
        self.key_word = key_w
        self.pos_dic = pos
        self.neg_dic = neg
    
    def special_filter(self,txt):
        spliter = self.key_word.upper()
        txt = spliter+txt.upper().split(spliter)[-1].split("$")[0]
        return txt
    
    def effective_ttr(self,xfile,thd):
        if len(xfile)==0:return None
        xfile["Datetime"] =pd.to_datetime(xfile.Created)
        xfile["Hour"] = xfile.Datetime.dt.hour
        xfile=xfile.sort_values(by="Datetime")
        # filter the effective user twitter
        x_effc = xfile[xfile.User_flr>=thd]
        x_effc.index = range(len(x_effc))
        # split the $ sign and get only the key word
        x_effc["fText"] = list(map(self.special_filter,x_effc.Text))
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
        if e_file is None:return None
        
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
        save_file = s_file.loc[:,["EST","User_name","Text","Sentiment","Created","User_flr",]]
        pos_tweets = save_file[save_file.Sentiment==1]
        neg_tweets = save_file[save_file.Sentiment==-1]
        return hour_count,pos_tweets,neg_tweets

    
    def get_all_senti(self,files,thres,is_log,is_save_senti):
        key_word = self.key_word
        #make other functions use these variables
        dates = [i[-14:-4] for i in files]
        # count sentiments
        all_sentis = pd.DataFrame()

        for i in range(len(dates)):
            idate = dates[i]
            ifile = files[i]
            xfile=pd.read_csv(ifile)
            # if empty, goes to next date file
            if len(xfile)==0:
                print("file is empty for {0}".format(idate))
                continue 

            e_file = self.effective_ttr(xfile,thres)
            isenti,pos_tweets,neg_tweets = self.senti_count(e_file,is_log)
            isenti.index = list(map(lambda x:pd.to_datetime(idate+" "+str(x)+":00:00"),isenti.index))
            all_sentis = pd.concat([all_sentis,isenti])
            # save the divided files if necessary
            if is_save_senti:
                senti_path = "results\\{0}".format(key_word)
                if not os.path.exists(senti_path):
                    os.makedirs(senti_path)
                if len(pos_tweets) != 0 :
                    pos_tweets.to_csv(senti_path+"\\{0}_{1}_pos.csv".format(key_word,idate))
                if len(neg_tweets) != 0 :
                    neg_tweets.to_csv(senti_path+"\\{0}_{1}_neg.csv".format(key_word,idate))
            
        print("sentiment files are saved successfully")
        all_sentis = all_sentis.replace([np.inf,-np.inf],[np.nan,np.nan])
        # convert all_sentis from UTC time to EST time
        all_sentis["EST"] = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in all_sentis.index]
        all_sentis.index = list(map(lambda x:x.replace(tzinfo=None),all_sentis["EST"]))
        # add net sentiment
        all_sentis["NetSentiment"] = all_sentis.Positive + all_sentis.Negative

        return all_sentis