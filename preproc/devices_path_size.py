import pandas as pd
from os import chdir
import gc
import sys
sys.path.append("preproc/libs/")
from location_path import GeoPath


def remove_bad_locations(events):
	# REMOVING BAD LOCATIONS #
	events = events[ (events["longitude"] != 0.0) & (events["latitude"] != 0.0) ]
	events = events[ (events["longitude"] != 1.0) & (events["latitude"] != 1.0) ]
	events = events[ (events["longitude"] != 104.0) & (events["latitude"] != 30.0) ]
	return events

def partition_weekend(events):
	weekend_config = (events["weekday"] == "sunday") | (events["weekday"] == "saturday") | ( (events["weekday"] == "friday") & (events["daytime"] == "dinner") ) | ( (events["weekday"] == "friday") & (events["daytime"] == "night" ) )
	ev_week    = events[ ~weekend_config ]
	del ev_week["daytime"]
	del ev_week["weekday"]
	ev_weekend = events[ weekend_config ]
	del ev_weekend["daytime"]
	del ev_weekend["weekday"]
	return {"week": ev_week, "weekend": ev_weekend}

working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"
dataset = "train"

chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}

events = pd.read_csv(data_dir + "/events_v2.csv", dtype=dtypes, sep=";")
del events["event_id"]
events = remove_bad_locations(events)
gc.collect()

events_partition = partition_weekend(events)
events = None
gc.collect()

ev_week = events_partition["week"]
ev_week = ev_week.sort_values(['device_id', 'timestamp'], ascending=[True, True])

ev_weekend = events_partition["weekend"]
ev_weekend = ev_weekend.sort_values(['device_id', 'timestamp'], ascending=[True, True])


#checking GeoPath
#a = ev_week[37:49]
#gp = GeoPath(a)

