
from collections import Counter
import pandas as pd
from glob import glob
import re

def calculate_top_words(result_path,topn):
    """ get top word
    """
    stopword = pd.read_csv("dictionary\\twitter_stopwords.txt",index_col=0).iloc[:,0].values
    pos_files=glob(result_path+"*pos*")
    neg_files=glob(result_path+"*neg*")
    pos_words,neg_words = "",""

    for i in range(len(pos_files)):
        ipos = pd.read_csv(pos_files[i])
        pos_words+= ipos.Text.sum().upper()

    for i in range(len(neg_files)):
        ineg = pd.read_csv(neg_files[i])
        neg_words+= ineg.Text.sum().upper()
            

    pos_dic = Counter(re.split('[^a-zA-Z]+', pos_words))
    neg_dic = Counter(re.split('[^a-zA-Z]+', neg_words))

    for w in pos_dic.keys():
        if w in stopword:
            pos_dic[w] = -1

    for w in pos_dic.keys():
        if w in stopword:
            neg_dic[w] = -1

    
    pos_df = pd.DataFrame(pos_dic.most_common())
    neg_df = pd.DataFrame(neg_dic.most_common())

    word_df = pd.concat([pos_df,neg_df],axis=1,join="outer")
    word_df.columns = ["positive_word","positive_count","negative_word","negative_count"]

    return word_df

def show_top(result_path,key_word,topn,show_flag):
    top_word = calculate_top_words(result_path,topn)
    top_word.to_csv(f'{result_path}{key_word}_topwords.csv')
    if show_flag:print(top_word.iloc[:topn,:])

if __name__ == "__main__":
    
    print(re.split('[^a-zA-Z]+', "s $ss 12 @@ x"))