#Script to group (gender, age) by location (longitude, latidude)
#Note that 2 decimal numbers at coordinates separates 1,1km

#Maybe group also by timestamp (rounding?)

import pandas as pd
from os import chdir
import gc

working_dir = "/home/tales/development/kaggle-talking-data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str}

events = pd.read_csv("data/events.csv", dtype=dtypes)
len(events)
events.head()
gender_age = pd.read_csv("data/gender_age_train.csv", dtype=dtypes)
len(gender_age)
gender_age.head()

group_loc = pd.merge(events, gender_age, on='device_id', how='left')
del group_loc['device_id']
del group_loc['event_id']
events = None
gender_age = None
gc.collect()

grouped_by_loc = group_loc.groupby(["longitude", "latitude"])

for group in grouped_by_loc:
	#due to python way to represent decimals, it changes (a little bit) the number
	#rounding back to 2 decimals can fix this
	group_lon = round(group[0][0], 2)
	group_lat = round(group[0][1], 2)
	group_df = group[1]
	print group_lon, group_lat
	print group_df
	print
	print ">>>", group_df.group.value_counts()
	print "---"
	print

#Henrique, if you check this out you'll see how amazing this featrue could be!! :D
#Incomplete, but I intend to make a csv with group (gender-age) relative frequencies and the absolute sum
#Once this csv is done, it can be used to get frequencies of neighbors location, example (12.34, 11.11) is in (12.33, 11.11) neighborhood 

