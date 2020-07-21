import pandas as pd
import numpy as np
import time
import datetime
import os



def countdown(t):
    #wait for another 15 mins
    t=t*60+1
    print("Twitter fetch data rate limit exceeded! Wait for another 15min...")
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1