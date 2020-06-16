import pandas as pd
import numpy as np
import datetime
import myhelper

now_time = datetime.datetime.today()
period = 3 # news in n hours
until_when = now_time



if __name__ == "__main__":
    
    newsdic = dict()
    request_counter = 0
    api = myhelper.api_load()
    names = pd.read_csv('dictionary\\PressName.csv').iloc[:,-1].values

    for iname in names:
        last_maxid =None
        time_gap = 0
        result = []
        while time_gap < period:
            time_line = api.user_timeline(iname,max_id=last_maxid, until = until_when)
            last_maxid=time_line[-1].id
            result += list(map(lambda x:(str(x.created_at),x.text),time_line))
            time_gap = (now_time - time_line[-1].created_at).seconds/3600
            if request_counter >= 179:
                    myhelper.countdown(16*60)
                    request_counter = 0
        newsdic[iname] = result

    pass

