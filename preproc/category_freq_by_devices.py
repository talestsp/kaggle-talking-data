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

app_labels = pd.read_csv("data/app_labels_ready.csv", dtype=dtypes, sep=";")

app_events = pd.merge(app_events, app_labels, on='app_id', how='left')
#del app_events["app_id"]
#gc.collect()


def cat_label_freq(df):
	return df["label_id"].value_counts()

def unique_app_ids(df):
	return len(df["app_id"].drop_duplicates())






#app_events = app_events.sort(by=[""])
#app_events.groupby(by="event_id").apply(cat_label_freq)
#app_events.head(20).groupby(by="event_id").apply(cat_label_freq)




#events = pd.read_csv(data_dir + "/events_v2.csv", dtype=dtypes, sep=";")
#del events["longitude"]
#del events["latitude"]
#del events["timestamp"]
#del events["daytime"]
#del events["weekday"]
#gc.collect()

