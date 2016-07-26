import pandas as pd
from os import chdir
import gc

working_dir = "/home/tales/development/kaggle-talking-data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str}


##### TABLES MERGED BY < device_id > IN events #####
##### inside this section, all merges had considered the gender_age key (device_id)

events = pd.read_csv("data/events.csv", dtype=dtypes)

gender_age = pd.read_csv("data/gender_age_test.csv", dtype=dtypes)
gender_age.head()
events = pd.merge(events, gender_age, on='device_id', how='inner')
events.head()
gender_age = None
gc.collect()

phone_brand = pd.read_csv("data/phone_brand_device_model_translated.csv", dtype=dtypes)
events = pd.merge(events, phone_brand, on='device_id', how='left')
phone_brand = None
gc.collect()
events.head()

events_test = events.event_id.drop_duplicates()

##### TABLES MERGED BY < app_id > IN app_events #####
##### inside this section, all merges had considered the app_events key (app_id)

app_labels = pd.read_csv("data/app_labels.csv", dtype=dtypes)
len(app_labels)
app_labels = app_labels.drop_duplicates()
len(app_labels)

label_categ = pd.read_csv("data/label_categories.csv", dtype=dtypes)
len(label_categ)
label_categ = label_categ.drop_duplicates()
len(label_categ)

app_categ = pd.merge(app_labels, label_categ, on='label_id', how='left')
len(app_categ)
app_categ = app_categ.drop_duplicates()
len(app_categ)
del app_categ['label_id']
app_labels = None
label_categ = None
gc.collect()

app_events = pd.read_csv("data/app_events.csv", dtype=dtypes)
len(app_events)
app_events = app_events[app_events.event_id.isin(events_test)]
len(app_events)
app_events.head()
app_events = pd.merge(app_events, app_categ, on='app_id', how='left')
del app_events['app_id']
del app_events['is_installed']
app_categ = None
gc.collect()
app_events = app_events.drop_duplicates()
app_events.head()
len(app_events)


##### TABLES MERGED #####

events = pd.merge(events, app_events, on='event_id', how='left')
del events['event_id']
app_events = None
gc.collect()
events = events.drop_duplicates()
len(events)
events.head()
len(events)

events.to_csv("data/test_events_full_basic.csv", index=False, sep=";")


exit()
