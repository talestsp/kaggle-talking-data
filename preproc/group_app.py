import pandas as pd
from os import chdir
import gc

working_dir = "/home/tales/development/kaggle-talking-data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": str, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str}

app_labels = pd.read_csv("data/app_labels.csv", dtype=dtypes)
app_labels = app_labels.drop_duplicates()

label_categ = pd.read_csv("data/label_categories.csv", dtype=dtypes)
label_categ = label_categ.drop_duplicates()

app_categ = pd.merge(app_labels, label_categ, on='label_id', how='left')
app_categ = app_categ.drop_duplicates()
app_categ.head()

del app_categ['label_id']
app_labels = None
label_categ = None
gc.collect()
app_categ.head()

events = pd.read_csv("data/events.csv", dtype=dtypes)
events.head()
del events['longitude']
del events['latitude']
del events['timestamp']
gc.collect()
events.head()

gender_age = pd.read_csv("data/gender_age_train.csv", dtype=dtypes)
gender_age.head()

events = pd.merge(events, gender_age, on='device_id', how='inner')
del events['device_id']
gc.collect()
events.head()

app_events = pd.read_csv("data/app_events.csv", dtype=dtypes)
app_events = pd.merge(events, app_events, on='event_id', how='inner')
del app_events['event_id']
del app_events['is_installed']
del app_events['is_active']
events = None
gc.collect()
app_events.head()

app_events = pd.merge(app_events, app_categ, on='app_id', how='left')
del app_events['app_id']
app_categ = None
gc.collect()
app_events.head()

gc.collect()
app_events.to_csv("data/group_app.csv", index=False, sep=";")


