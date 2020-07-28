import pandas as pd
import numpy as np
import time
import datetime
import os



def countdown(t):
    #wait for t mins

    print(f"Wait for {t} min...")
    t=int(t*60+1)
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1