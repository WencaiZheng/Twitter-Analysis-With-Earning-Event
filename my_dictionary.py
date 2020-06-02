
import pandas as pd
import numpy as np
import os

def my_dict():
    LM_dic = pd.read_csv("dictionary\\LoughranMcDonald_MasterDictionary_2018.csv")
    pos_dic = LM_dic[LM_dic.Positive!=0].Word.values
    neg_dic = LM_dic[LM_dic.Negative!=0].Word.values
    return pos_dic,neg_dic



if __name__ == "__main__":
    pass