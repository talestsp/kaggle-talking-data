import pandas as pd
from os import chdir
import gc

# Purpose: This script reads the file read 3 files, merge than by their common attributes, compute sum and mean for apps installed and active and create the file device_apps_ready.csv

# import sys
# sys.modules[__name__].__dict__.clear()
# gc.collect()

####################################################### Load Data ####################################################### 

working_dir = "/home/henrique/DataScience/talking_data"
chdir(working_dir)

dtypes = {"event_id": int, "device_id": str, "timestamp": str, "longitude": float, "latitude": float, "is_active": float, "is_installed": float, "app_id": str, "label_id": str, "category": str, "new_label_id": str}

app_events = pd.read_csv("data_files/app_events.csv", dtype=dtypes, sep=",")

app_labels = pd.read_csv("data_files_ready/app_custom_label.csv", dtype=dtypes, sep=";")

events = pd.read_csv("data_files_ready/events_ready.csv", dtype=dtypes, sep=";")

len(events['device_id'].unique())

####################################################### Prepare Data #######################################################

app_events = pd.merge(app_events, app_labels, how='left', on='app_id')

app_labels = None

app_events = app_events[["event_id", "new_label_id", "is_installed", "is_active"]]

app_events = app_events.groupby(["event_id", "new_label_id"]).agg(sum).reset_index()

app_events = pd.merge(app_events, events, how='left', on='event_id')

events = None

gc.collect()

app_events = app_events[["device_id", "new_label_id", "is_installed", "is_active", "timestamp"]]

######################################################## Save Data #######################################################

app_events.to_csv("data_files_ready/device_apps_ready.csv", sep = ";", index=False)

