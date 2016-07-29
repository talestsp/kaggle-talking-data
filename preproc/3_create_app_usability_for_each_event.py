import pandas as pd
from os import chdir
import gc

# Purpose: This script reads the file app_labels_ready, create an unique category for each label_id and save it in a new file named app_labels_final.csv

# import sys
# sys.modules[__name__].__dict__.clear()
# gc.collect()

####################################################### Load Data ####################################################### 

working_dir = "/home/henrique/DataScience/talking_data"
chdir(working_dir)

dtypes = {"event_id": int, "device_id": str, "timestamp": str, "longitude": float, "latitude": float, "is_active": float, "is_installed": float, "app_id": str, "label_id": str, "category": str}

# app_event_columns = ["event_id", "app_id", "is_installed", "is_active"]

app_events = pd.read_csv("data_files/app_events.csv", dtype=dtypes, sep=",")

app_labels = pd.read_csv("data_files_ready/app_custom_label.csv", dtype=dtypes, sep=";")

events = pd.read_csv("data_files_ready/events_ready.csv", dtype=dtypes, sep=";")

# device_id_map = pd.DataFrame(events["device_id"])

# device_id_map["device_new_id"] = LabelEncoder().fit_transform(device_id_map.device_id)


####################################################### Functions #######################################################

app_events = pd.merge(app_events, app_labels, how='left', on='app_id')

app_events = app_events[["event_id", "new_label_id", "is_installed", "is_active"]]

app_events = app_events.groupby(["event_id", "new_label_id"]).agg(sum).reset_index()

app_events = pd.merge(app_events, events, how='left', on='event_id')

app_events = app_events[["device_id", "new_label_id", "is_installed", "is_active", "timestamp"]]

app_events = app_events.groupby(["device_id", "new_label_id", "timestamp"]).mean().reset_index()

app_events




app_events = app_events.sort_values(['device_id', 'new_label_id'], ascending=[1,0])













# ####################################################### Execution #######################################################

# app_labels = app_labels.groupby(["app_id"]).agg(custom_merge).reset_index()

# general_categories_list = app_labels['label_id'].value_counts().index.tolist()
            
# app_labels['new_label_id'] = app_labels['label_id'].apply(transform_groups_to_numbers)

# ####################################################### Save Data #######################################################

# app_labels.to_csv("data_files_ready/app_labels_ready2.csv", sep = ";", index=False)

