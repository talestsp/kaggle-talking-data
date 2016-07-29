import pandas as pd
from os import chdir
import gc
import sys
import datetime

####################################################### Load Data ####################################################### 

working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"

#working_dir = sys.argv[1]
#data_dir = sys.argv[2]
chdir(working_dir)

dtypes = {"event_id": int, "device_id": str, "timestamp": str, "longitude": float, "latitude": float}

events = pd.read_csv(data_dir + "/events.csv", dtype=dtypes)
len(events)
events = events.drop_duplicates()
len(events)

####################################################### Functions ####################################################### 

def extract_hour(datetime):
    datetime = datetime[11:13]
    return(int(datetime))

def set_day_time(hour):
    if (hour < 6):
        return("dawn")
    if (6 <= hour & hour < 8):
        return("breakfast")
    if (8 <= hour & hour < 12):
        return("morning")
    if (12 <= hour & hour < 14):
        return("lunch")
    if (14 <= hour & hour < 18):
        return("afternoon")
    if (18 <= hour & hour < 20):
        return("dinner")
    else: # (20 <= hour && hour < 0) {
        return("night")

def set_weekday(timestamp):
    WEEKDAY = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"}
    pd.tslib.Timestamp(timestamp)
    n_weekday = timestamp.weekday()
    return WEEKDAY[n_weekday]

####################################################### Execution ####################################################### 

events["daytime"] = events["timestamp"].apply(extract_hour)

events = events.sort_values(['daytime'], ascending=True)

events["daytime"] = events["daytime"].apply(set_day_time)

events = events.sort_values(['event_id'], ascending=True)

events["weekday"] = pd.to_datetime(events["timestamp"]).apply(set_weekday)
####################################################### Save Data ####################################################### 

events.to_csv(data_dir + "/events_v2.csv", sep = ";", index=False)

