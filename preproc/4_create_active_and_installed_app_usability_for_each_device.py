import pandas as pd
from os import chdir
import gc
from sklearn.preprocessing import LabelEncoder

# Purpose: read "device_apps_ready.csv", create columns with top apps information for each device and saves it in the file "device_top_apps_prediction_ready.csv"

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

# concat and count top installed app categories 
device_top_intalled_apps = device_top_intalled_apps.groupby(["device_id"])["new_label_id"].agg({"top_3_installed_apps": lambda x: ",".join(x.tolist()[0:3]), "top_2_installed_apps": lambda x: ",".join(x.tolist()[0:2]), "top_1_installed_app": lambda x: ",".join(x.tolist()[0:1]), 'distinct_app_categories': 'count'}).reset_index()

# concat and count top active app categories
device_top_active_apps = device_top_active_apps.groupby(["device_id"])["new_label_id"].agg({"top_3_active_apps": lambda x: ",".join(x.tolist()[0:3]), "top_2_active_apps": lambda x: ",".join(x.tolist()[0:2]), "top_1_active_app": lambda x: ",".join(x.tolist()[0:1]), 'distinct_active_app_categories': 'count'}).reset_index()

#merge two lists - WARNING: This generates some NaN as device_top_intalled_apps has more rows than device_top_active_apps

device_top_intalled_apps = pd.merge(device_top_intalled_apps, device_top_active_apps, how='left', on='device_id')

device_top_intalled_apps[pd.isnull(device_top_intalled_apps.distinct_active_app_categories)]

device_top_intalled_apps.top_3_installed_apps = LabelEncoder().fit_transform(device_top_intalled_apps.top_3_installed_apps)
device_top_intalled_apps.top_3_active_apps = LabelEncoder().fit_transform(device_top_intalled_apps.top_3_active_apps)

device_top_intalled_apps.top_2_installed_apps = LabelEncoder().fit_transform(device_top_intalled_apps.top_2_installed_apps)
device_top_intalled_apps.top_2_active_apps = LabelEncoder().fit_transform(device_top_intalled_apps.top_2_active_apps)

######################################################## Save Data #######################################################

device_top_intalled_apps.to_csv("data_files_ready/device_top_apps_prediction_ready.csv", sep = ";", index=False)


