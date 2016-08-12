#this script returns the path size mean divided by number of days
#it was used the euclidean distance

import pandas as pd
from os import chdir
import gc
import sys
working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"
chdir(working_dir)
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
	ev_week = events[ ~weekend_config ]
	del ev_week["daytime"]
	del ev_week["weekday"]
	ev_weekend = events[ weekend_config ]
	del ev_weekend["daytime"]
	del ev_weekend["weekday"]
	return {"week": ev_week, "weekend": ev_weekend}

def devices_path_weight(ev):
	devices = ev.device_id.drop_duplicates()
	devices_path_weight = []
	counter = 0
	len_devices = len(devices)
	for dev in devices:
		counter = counter + 1
		print len_devices, counter
		dev_df = ev[ ev["device_id"] == dev ]
		dev_df = dev_df.sort_values(['device_id', 'timestamp'], ascending=[True, True])
		dev_gp = GeoPath(dev_df)
		path_weight = dev_gp.path_weight()
		n_days = len(dev_gp.distinct_days(dev_df.timestamp))
		devices_path_weight.append({"device_id": dev, "path_weight": path_weight, "path_weight_by_days": path_weight / n_days})
	return devices_path_weight

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

path_week = devices_path_weight(ev_week)
path_weekend = devices_path_weight(ev_weekend)

path_week = pd.DataFrame(path_week)
path_weekend = pd.DataFrame(path_weekend)

path_week.to_csv(data_dir + "path_weight_week.csv")
path_weekend.to_csv(data_dir + "path_weight_weekend.csv")

path_week.path_weight.describe()
path_week.path_weight_by_days.describe()

path_weekend.path_weight.describe()
path_weekend.path_weight_by_days.describe()

exit()

