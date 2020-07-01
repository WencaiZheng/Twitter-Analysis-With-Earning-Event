import pandas as pd
import numpy as np
import time
import datetime
import os



def countdown(t):
    print("Rate limit exceed! wait for another 16min...if you believe this is abnormal, check code")
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1