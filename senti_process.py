
import pandas as pd
import numpy as np
import os




def effective_ttr(xfile,influencer_threshold=20):
    if len(xfile)==0:return None
    xfile["Datetime"] =pd.to_datetime(xfile.Created)
    xfile["Hour"] = xfile.Datetime.dt.hour
    xfile=xfile.sort_values(by="Datetime")
    # filter the effective user twitter
    x_effc = xfile[xfile.User_flr>=influencer_threshold]
    x_effc.index = range(len(x_effc))
    return x_effc

def get_senti(rawtxt):
    txt = rawtxt.upper()
    txt_list= txt.split(" ")
    pos_count,neg_count =0,0
    for i in txt_list:
        if i in pos_dic:pos_count+=1
        if i in neg_dic:neg_count+=1
    # positive
    if pos_count>neg_count:senti = 1
    elif pos_count<neg_count:senti = -1
    else: senti = 0
    return senti

def senti_count(e_file,log_flag):

    """count how many positive or negative in a file named e_file
        log_flag: whether or not scale the count into log
    """
    if e_file is None:return None
    sentis = list(map(get_senti,e_file.Text))
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
    save_file = s_file.loc[:,["EST","User_name","Text","Sentiment","Created","User_flr"]]
    pos_tweets = save_file[save_file.Sentiment==1]
    neg_tweets = save_file[save_file.Sentiment==-1]
    return hour_count,pos_tweets,neg_tweets

def get_all_senti(key_word,files,pos_dic_,neg_dic_,influencer_threshold_,log_flag_,save_senti_flag):
    #make other functions use these variables
    global pos_dic,neg_dic,log_flag,influencer_threshold
    # define
    pos_dic,neg_dic = pos_dic_,neg_dic_
    log_flag,influencer_threshold = log_flag_,influencer_threshold_

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

        e_file = effective_ttr(xfile)
        isenti,pos_tweets,neg_tweets = senti_count(e_file,log_flag)
        isenti.index = list(map(lambda x:pd.to_datetime(idate+" "+str(x)+":00:00"),isenti.index))
        all_sentis = pd.concat([all_sentis,isenti])
        # save the divided files if necessary
        if save_senti_flag:
            senti_path = "results\\{0}".format(key_word)
            if not os.path.exists(senti_path):
                os.makedirs(senti_path)
            if len(pos_tweets) !=0 :
                pos_tweets.to_csv(senti_path+"\\{0}_{1}_pos.csv".format(key_word,idate))
            if len(neg_tweets) !=0 :
                neg_tweets.to_csv(senti_path+"\\{0}_{1}_neg.csv".format(key_word,idate))
        
    print("sentiment files are saved successfully")
    all_sentis = all_sentis.replace([np.inf,-np.inf],[np.nan,np.nan])
    # convert all_sentis from UTC time to EST time
    all_sentis["EST"] = [i.tz_localize('UTC').tz_convert('US/Eastern') for i in all_sentis.index]
    all_sentis.index = list(map(lambda x:x.replace(tzinfo=None),all_sentis["EST"]))
    # add net sentiment
    all_sentis["NetSentiment"] = all_sentis.Positive + all_sentis.Negative

    return all_sentis