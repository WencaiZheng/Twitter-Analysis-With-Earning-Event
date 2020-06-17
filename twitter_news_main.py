import pandas as pd
import numpy as np
import datetime
import myhelper
import os 


now_time = datetime.datetime.today()
period = 8  # news in n hours



if __name__ == "__main__":

    full_df = pd.DataFrame()
    request_counter = 0
    api = myhelper.api_load()
    names = pd.read_csv('dictionary\\PressName.csv').iloc[:,-1].values

    for iname in names:
        last_maxid = None
        time_gap = -1
        result = []
        while time_gap < period:

            request_counter += 1
            time_line = api.user_timeline(iname,max_id=last_maxid,)
            if len(time_line) == 0:
                time_gap = period+1
                continue

            last_maxid=time_line[-1].id
            result += list(map(lambda x:(str(x.created_at),x.text),time_line))
            time_gap = (now_time - time_line[-1].created_at).days
            print(request_counter,iname,time_line[-1].created_at)
            
            # reach limit
            if request_counter >= 179:
                myhelper.countdown(16*60)
                request_counter = 0

        result_df = pd.DataFrame(result,columns=['Time',iname])
        full_df = pd.concat([full_df,result_df],sort=False,axis =1,join='outer')

    #write one day before because of twitter setting
    save_path = 'news\\'
    # if path not exit, create folders
    if not os.path.exists(save_path):os.makedirs(save_path)
    full_df.to_csv('news\\corona.csv')

