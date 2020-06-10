import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
import requests
import re
from bs4 import BeautifulSoup
import time
from collections import Counter

head_url ="https://finance.yahoo.com"

def get_earnings_info(ticker):

    the_url = head_url+f'/calendar/earnings?symbol={ticker}'
    # fake a header of a browser
    headers = {'User-Agent': 'Chrome/39.0.2171.95'}
    response = requests.get(the_url, headers=headers)
    # beatifulsoup find all the right tags
    soup = BeautifulSoup(response.text, features='lxml')

    eraning_time=soup.find_all(attrs={"aria-label": "Earnings Date"})
    est_eps=soup.find_all(attrs={"aria-label": "EPS Estimate"})
    rpt_eps=soup.find_all(attrs={"aria-label": "Reported EPS"})
    surprise =soup.find_all(attrs={"aria-label": "Surprise(%)"})

    earning_release_time = list(map(lambda x:pd.to_datetime(x.text[:-3]),eraning_time))
    estimated_eps = list(map(lambda x:x.text,est_eps))
    reported_eps = list(map(lambda x:x.text,rpt_eps))
    surprise_percentage = list(map(lambda x:x.text,surprise))

    earning_release = pd.DataFrame([earning_release_time,estimated_eps,reported_eps,surprise_percentage]).T
    earning_release.columns = ["EarningsDate","EstimateEPS","ReportedEPS","Surprise"]
    earning_release.set_index("EarningsDate",drop=True,inplace=True)
    earning_release.replace("N/A",np.nan,inplace=True)
    earning_release = earning_release.astype(float)

    if len(earning_release)==0:print("No Earning date found for {},check ticker".format(ticker))
    print("Earning dates scraped successfully")   
    return earning_release

def get_general_news(ticker):
    the_url = f'{head_url}/quote/{ticker}/news?p={ticker}'
    # fake a header of a browser
    headers = {'User-Agent': 'Chrome/39.0.2171.95'}
    response = requests.get(the_url, headers=headers)
    # beatifulsoup find all the right tags
    soup = BeautifulSoup(response.text, features='lxml')
    inews = soup.find_all(href=re.compile("news.*"+ticker.lower()))
    # if key word is in the website address
    key_url = [(i.text,i.get('href')) if ".com" in i.get('href') else (i.text,head_url+i.get('href')) for i in inews]
    key_url_df = pd.DataFrame(key_url,columns=["Headlines","Newslink"])

    return key_url_df

if __name__ == "__main__":
    start_date="2020-04-26"
    end_date="2020-05-02"
    ticker = "IQ"
    tics=["BILI","IQ","HUYA","MOMO","DOYU","NFLX","WB"]
    alls=pd.DataFrame()
    for ticker in tics:
        key_dict_e = get_earnings_info(ticker)
        alls = pd.concat([alls,key_dict_e])
    alls.to_csv("C:\\Users\\wenca\\Desktop\\epss.csv")