
import pandas as pd
import numpy as np
from glob import glob
import os

import processor._senti_process as senti_process
#change it to the address where the file is located in your computer
os.chdir('C:\\Users\\wenca\\Desktop\\GitRepo\\Twitter-Analysis-With-Earning-Event\\')

class TwitterDict:
    """This is the dictionary from McDonald's paper
    But here we added some new words that fit twitter more
    """
    my_dict = pd.read_csv('dictionary\\MyDict.csv')
    my_pos = my_dict.Positive.dropna().values
    my_neg = my_dict.Negative.dropna().values

    @staticmethod
    def origin_dict():
        LM_dic = pd.read_csv("dictionary\\LoughranMcDonald_MasterDictionary_2018.csv")
        pos_dic = LM_dic[LM_dic.Positive!=0].Word.values
        neg_dic = LM_dic[LM_dic.Negative!=0].Word.values
        return pos_dic,neg_dic

    @classmethod
    def new_dict(cls):
        my_pos,my_neg = cls.my_pos,cls.my_neg
        pos_dic,neg_dic = cls.origin_dict()
        new_pos = np.append(pos_dic,my_pos)
        new_neg = np.append(neg_dic,my_neg)
        return new_pos,new_neg



if __name__ == "__main__":
    
    pos,neg = TwitterDict().new_dict()

    key_word = "$WORK"
    keyword_path = f"twitters\\{key_word}\\" # where the raw twitters are stored
    # read all files
    files=glob(f'{keyword_path}*{key_word}*')
    ifile=files[-1]
    xfile=pd.read_csv(ifile)
    test_obj = senti_process.SentiProcess(key_word,pos,neg)

    e_file = test_obj.effective_ttr(xfile,thd=10)
    isenti,pos_tweets,neg_tweets = test_obj.senti_count("2020-05-01",e_file,log_flag=0)
    
    print(pos_tweets)
    print(neg_tweets)
