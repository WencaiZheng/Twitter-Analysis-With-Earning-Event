
import pandas as pd
import numpy as np
import os

class TwitterDict:

    my_pos = ["BELIEVER"]
    my_neg = []

    @staticmethod
    def origin_dict():
        LM_dic = pd.read_csv("dictionary\\LoughranMcDonald_MasterDictionary_2018.csv")
        pos_dic = LM_dic[LM_dic.Positive!=0].Word.values
        neg_dic = LM_dic[LM_dic.Negative!=0].Word.values
        return pos_dic,neg_dic

    @classmethod
    def new_dict(cls):
        my_pos,my_neg = np.array(cls.my_pos),np.array(cls.my_neg)
        pos_dic,neg_dic = cls.origin_dict()
        new_pos = np.append(pos_dic,my_pos)
        new_neg = np.append(neg_dic,my_neg)
        return new_pos,new_neg



if __name__ == "__main__":
    os.chdir("Twitter-Analysis-With-Earning-Event\\")
    x,y=TwitterDict().new_dict()
    print(x)
    pass