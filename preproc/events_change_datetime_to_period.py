import pandas as pd
from os import chdir
import gc

####################################################### Load Data ####################################################### 

working_dir = "/home/henrique/DataScience/talking_data"
chdir(working_dir)

dtypes = {"event_id": int, "device_id": str, "timestamp": str, "longitude": float, "latitude": float}

selected_columns = ["event_id", "device_id", "timestamp"]

events = pd.read_csv("data_files/events.csv", dtype=dtypes, usecols=selected_columns)
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

####################################################### Execution ####################################################### 

events["timestamp"] = events["timestamp"].apply(extract_hour)

events = events.sort_values(['timestamp'], ascending=True)

events["timestamp"] = events["timestamp"].apply(set_day_time)

events = events.sort_values(['event_id'], ascending=True)

####################################################### Save Data ####################################################### 

events.to_csv("data_files_ready/events_ready.csv", sep = ",", index=False)

