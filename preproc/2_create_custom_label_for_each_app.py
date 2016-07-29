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

dtypes = {"event_id": int, "device_id": str, "timestamp": str, "longitude": float, "latitude": float, "is_active": int, "is_installed": int, "app_id": str, "label_id": str, "category": str}

app_labels = pd.read_csv("data_files_ready/app_labels_ready.csv", dtype=dtypes, sep=";")

####################################################### Functions #######################################################

# concat categories from each label_id to create an unique category
def custom_merge(column):
    row = ""
    for i in column:
        row = row + i + ","
    row = row[:-1]
    return (row)

def transform_groups_to_numbers(x):
    for idx, group in enumerate(general_categories_list):
        if x == group:
            return(idx + 1)

####################################################### Execution #######################################################

app_labels = app_labels.groupby(["app_id"]).agg(custom_merge).reset_index()

general_categories_list = app_labels['label_id'].value_counts().index.tolist()
            
app_labels['new_label_id'] = app_labels['label_id'].apply(transform_groups_to_numbers)

####################################################### Save Data #######################################################

app_labels.to_csv("data_files_ready/app_labels_ready2.csv", sep = ";", index=False)

