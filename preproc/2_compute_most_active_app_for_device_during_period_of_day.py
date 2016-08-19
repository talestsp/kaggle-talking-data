import pandas as pd
from os import chdir
import gc
from sklearn.preprocessing import LabelEncoder

# Purpose: This script compute the app that is most active during a day period for each device and saves it in the file device_top_active_apps_by_period.csv

# import sys
# sys.modules[__name__].__dict__.clear()
# gc.collect()

####################################################### Load Data ####################################################### 

# working_dir = "/home/henrique/DataScience/talking_data"
working_dir = "C:/Users/Desenvolvedores/Documents/DataScience/talking_data"

chdir(working_dir)

dtypes = {"event_id": int, "device_id": str, "timestamp": str, "longitude": float, "latitude": float, "is_active": float, "is_installed": float, "app_id": str, "label_id": str, "category": str, "new_label_id": str}

app_events = pd.read_csv("data_files/app_events.csv", dtype=dtypes, 
                        # nrows=3000000,
                        sep=",", usecols=['event_id','app_id','is_active'])

events = pd.read_csv("data_files_ready/events_ready.csv", dtype=dtypes, sep=";")

####################################################### Prepare Data #######################################################

app_events = pd.merge(events, app_events, how='inner', on='event_id')

app_events = app_events[["device_id", "timestamp", "app_id", "is_active"]]

app_events = app_events.groupby(['device_id', 'timestamp', 'app_id'])['is_active'].agg({'active_times':'sum'}).reset_index()

app_events = app_events.sort_values(['device_id', 'timestamp', 'active_times'], ascending=[1,0,0])

app_events = app_events.groupby(['device_id', 'timestamp'], as_index=False).first()

app_events.app_id = LabelEncoder().fit_transform(app_events.app_id)

######################################################## Save Data #######################################################

app_events.to_csv("data_files_ready/device_top_active_apps_by_period.csv", sep = ";", index=False)


