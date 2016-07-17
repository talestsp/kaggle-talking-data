import pandas as pd
from os import chdir
import gc

working_dir = "/home/tales/development/kaggle-talking-data/"
chdir(working_dir)

dtypes = {'label_id': str, 'category': str, "app_id": str, "event_id": str, "app_id": str, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str}

app_labels = pd.read_csv("data/app_labels.csv", dtype=dtypes)
label_categ = pd.read_csv("data/label_categories.csv", dtype=dtypes)

app_categ = pd.merge(app_labels, label_categ, on='label_id')
del app_categ['label_id']
app_labels = None
label_categ = None
gc.collect()


app_events = pd.read_csv("data/app_events.csv", dtype=dtypes)
app_events = pd.merge(app_events, app_categ, on='app_id')
del app_events['app_id']
gc.collect()
app_events.head()
app_events.to_csv("data/app_events_merging.csv", index=False, sep=";")

app_event_groupby = app_events.groupby(['event_id', 'is_installed', 'is_active', 'category'])
result = app_event_groupby[['event_id', 'is_installed', 'is_active', 'category']].agg(['count'])

events = pd.read_csv("data/events.csv", dtype=dtypes)
app_events = pd.merge(app_events, events, on='event_id')

#incomplete...