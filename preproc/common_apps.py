#find and analyze the common apps to all groups

import pandas as pd
from os import chdir
import gc

working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}

app_events = pd.read_csv(data_dir + "/app_events.csv", dtype=dtypes)
del app_events["is_installed"]
del app_events["is_active"]
gc.collect()

gender_age = pd.read_csv(data_dir + "/gender_age_train.csv", dtype=dtypes)
del gender_age["gender"]
del gender_age["age"]
gc.collect()

events = pd.read_csv(data_dir + "/events.csv", dtype=dtypes)
del events["timestamp"]
del events["longitude"]
del events["latitude"]
gc.collect()

app_events = pd.merge(app_events, events, on='event_id', how='inner')
events = None
gc.collect()
app_events = pd.merge(app_events, gender_age, on='device_id', how='inner')

app_events.head()

def top_freq(column, n=1):
	return column.value_counts().head(n)

def n_events(column):
	return len(column)

freq_app_events_by_group = app_events.groupby(by="group")["app_id"].apply(top_freq)
sum_events_by_group = app_events[["device_id", "event_id", "group"]].drop_duplicates().group.value_counts()

#TODO set the mode of those event_sizes by device 
event_size_by_device = app_events.groupby(by=["device_id", "event_id"]).apply(n_events)
event_size_by_device.to_csv(data_dir + "event_size_by_device.csv", sep = ";")



