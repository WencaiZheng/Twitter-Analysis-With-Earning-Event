import pandas as pd
import numpy as np
import datetime
import os
import myhelper
api = myhelper.api_load()

class Filter:

    request_counter = 0
    @classmethod
    def freq_filter(cls,user_id):
        """return T or F
        """
        period = 1
        freq_thres = 10
        last_maxid = None
        result = []
        day_gap = 0 

        while day_gap<= period:
            time_line =api.user_timeline(user_id,max_id=last_maxid)
            cls.request_counter += 1
            last_maxid=time_line[-1].id
            result += list(map(lambda x:x.created_at,time_line))
            day_gap = (datetime.datetime.today() - time_line[-1].created_at).days
            # limit reached
            if cls.request_counter >= 179:
                myhelper.countdown(16*60)
                cls.request_counter = 0

        freq = sum(np.array(result)>(datetime.datetime.today()-datetime.timedelta(period)))
        return freq>=freq_thres

if __name__ == "__main__":
    # hello world
    pass