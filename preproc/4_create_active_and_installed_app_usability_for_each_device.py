import pandas as pd
from os import chdir
import gc
import math

# Purpose: 

# import sys
# sys.modules[__name__].__dict__.clear()
gc.collect()

####################################################### Load Data ####################################################### 

working_dir = "/home/henrique/DataScience/talking_data"
chdir(working_dir)

dtypes = {"event_id": int, "device_id": str, "timestamp": str, "longitude": float, "latitude": float, "is_active": float, "is_installed": float, "app_id": str, "label_id": str, "category": str, "new_label_id": str}

device_apps_ready = pd.read_csv("data_files_ready/device_apps_ready.csv", dtype=dtypes, sep=";")

####################################################### Prepare Data #######################################################


device_top_intalled_apps = device_apps_ready.groupby(["device_id", "new_label_id"]).mean().reset_index()

device_top_intalled_apps = device_top_intalled_apps.sort_values(['device_id', 'is_installed'], ascending=[1,0])

#remove apps that were never active
device_top_active_apps = device_top_intalled_apps.sort_values(['device_id', 'is_active'], ascending=[1,0])

device_top_active_apps = device_top_active_apps[device_top_active_apps.is_active != 0.0]

#select columns
device_top_intalled_apps = device_top_intalled_apps[["device_id", "new_label_id"]]

device_top_active_apps = device_top_active_apps[["device_id", "new_label_id"]]

####################################################### Functions #######################################################

# concat categories from each label_id to create an unique category
def custom_merge(column):
    row = ""
    for i in column:
        row = row + i + ","
    row = row[:-1]
    return (row)

#concat and count top installed app categories 
first = device_top_intalled_apps.groupby(["device_id"]).agg(lambda x: "|".join(x.tolist())).reset_index()

second = device_top_intalled_apps.groupby(["device_id"]).agg('count').reset_index()

device_top_intalled_apps = pd.merge(first, second, how='left', on='device_id')

device_top_intalled_apps.columns = ['device_id', 'top_installed_apps', 'distinct_app_categories']

#concat and count top active app categories 

first = device_top_active_apps.groupby(["device_id"]).agg(custom_merge).reset_index()

second = device_top_active_apps.groupby(["device_id"]).agg('count').reset_index()

device_top_active_apps = pd.merge(first, second, how='left', on='device_id')

device_top_active_apps.columns = ['device_id', 'top_active_apps', 'distinct_active_app_categories']

#merge two lists - WARNING: This generates some NaN as device_top_intalled_apps has more rows than device_top_active_apps

device_top_intalled_apps = pd.merge(device_top_intalled_apps, device_top_active_apps, how='left', on='device_id')

device_top_intalled_apps[pd.isnull(device_top_intalled_apps.distinct_active_app_categories)]
