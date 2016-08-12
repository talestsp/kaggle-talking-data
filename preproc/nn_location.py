#this script generates the group frequencies for each device considering 
#all its location during the morning and afternoon from monday to friday

import pandas as pd
from os import chdir
import gc
import sys
import numpy

working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}

'''
Returns the boundaries of the nearests location neighbors.
args:
	loc_base: location center
	delta: the radius from the loc_base that defines its neighborhood
'''
def get_boundaries(loc_base, delta):
	loc_base_lon = loc_base[0]
	loc_base_lat = loc_base[1]
	delta_lon = loc_base_lon - (delta), loc_base_lon + (delta)
	delta_lat = loc_base_lat - (delta), loc_base_lat + (delta)
	return delta_lon, delta_lat

def build_row(loc_base, device_neighbors, gender_age_factors):
	row = [loc_base[0], loc_base[1]]
	n_ocurrences = len(device_neighbors)
	freq = dict(device_neighbors.group.value_counts())
	for ga in gender_age_factors:
		if(ga in freq.keys()):
			#print ga, "\t", freq[ga]
			row.append(freq[ga])
		else:
			#print ga, "\t", 0
			row.append(0)
	row.append(n_ocurrences)
#	print [device_id] + gender_age_factors + ["total"]
#	print ">>>", row
	return row

def summarize_fres_by_device(device, device_freqs_by_loc, train_set=False, group=None):
	if (len(device_freqs_by_loc) > 0 and train_set == False):
		summarized = {}
		total = float(device_freqs_by_loc["nn.total"].sum())

		del device_freqs_by_loc["nn.total"]
		del device_freqs_by_loc["longitude"]
		del device_freqs_by_loc["latitude"]

		for column in device_freqs_by_loc.columns.values:
			summarized[column] = round(float(device_freqs_by_loc[column].sum() / total), 4)

		summarized["device_id"] = device

		return summarized

	if (len(device_freqs_by_loc) > 0 and train_set == True):
		summarized = {}
		total = float(device_freqs_by_loc["nn.total"].sum())

		del device_freqs_by_loc["nn.total"]
		del device_freqs_by_loc["longitude"]
		del device_freqs_by_loc["latitude"]

		for column in device_freqs_by_loc.columns.values:
			summarized[column] = round(float(device_freqs_by_loc[column].sum() / total), 4)

		summarized["device_id"] = device
		summarized["group"] = group

		return summarized



#### LOADING ####
events = pd.read_csv(data_dir + "/events_v2.csv", dtype=dtypes, sep=";")

gender_age = pd.read_csv("data/gender_age_train.csv", dtype=dtypes)
del gender_age['gender']
del gender_age['age']
#### END LOADING ####

events = pd.merge(events, gender_age, on='device_id', how='inner')
del events['timestamp']
del events['event_id']
del events['weekday']
del events['daytime']
events = events.drop_duplicates()
gc.collect()
gender_age_factors = list(gender_age.group.drop_duplicates().sort_values())

# REMOVING BAD LOCATIONS #
events = events[ (events["longitude"] != 0.0) & (events["latitude"] != 0.0) ]
events = events[ (events["longitude"] != 1.0) & (events["latitude"] != 1.0) ]
events = events[ (events["longitude"] != 104.0) & (events["latitude"] != 30.0) ]

devices = events.device_id.drop_duplicates()

#get the mos common neighbors' group for each device_id
counter = 1
freq_group_by_loc = []
for device_id in devices:
	print len(devices), counter
	df_device = events[ events["device_id"] == device_id ]
	for row in df_device.iterrows():
		row = row[1]
		loc_base = row["longitude"], row["latitude"]
		delta_lon, delta_lat = get_boundaries(loc_base, 0.01)
		device_neighbors = events[ 	(events.longitude >= delta_lon[0]) &
									(events.longitude <= delta_lon[1]) &
									(events.latitude  >= delta_lat[0]) &
									(events.latitude  <= delta_lat[1])]

		del device_neighbors['longitude']
		del device_neighbors['latitude']

		#remove same device ocurrences
		device_neighbors = device_neighbors.drop_duplicates()
		del device_neighbors["device_id"]

		freq_row = build_row(loc_base, device_neighbors, gender_age_factors)
		freq_group_by_loc.append(freq_row)
	counter = counter + 1

#events = None
#gc.collect()

freq_columns = ["longitude", "latitude", "nn.F23-", "nn.F24-26", "nn.F27-28", "nn.F29-32", "nn.F33-42", "nn.F43+", "nn.M22-", "nn.M23-26", "nn.M27-28", "nn.M29-31", "nn.M32-38", "nn.M39+", "nn.total"]
freq_df_by_loc = pd.DataFrame(freq_group_by_loc)
freq_df_by_loc.columns = freq_columns

#there are cases in which the same location has more than one device
#some cases they have the same neighbors (if they belong to the same group)
#so there are repeated rows
freq_df_by_loc = freq_df_by_loc.drop_duplicates()

### APPLYING TO TEST DATA ###
events_test = pd.read_csv(data_dir + "/events_v2.csv", dtype=dtypes, sep=";")
gender_age_test = pd.read_csv("data/gender_age_test.csv", dtype=dtypes)

events_test = pd.merge(events_test, gender_age_test, on='device_id', how='inner')
del events_test['timestamp']
del events_test['event_id']
del events_test['weekday']
del events_test['daytime']
events_test = events_test.drop_duplicates()
gc.collect()

devices_test = events_test.device_id.drop_duplicates()

events_test = events_test[ (events_test["longitude"] != 0.0) & (events_test["latitude"] != 0.0) ]
events_test = events_test[ (events_test["longitude"] != 1.0) & (events_test["latitude"] != 1.0) ]
events_test = events_test[ (events_test["longitude"] != 104.0) & (events_test["latitude"] != 30.0) ]

#calculating the frequencies for each device, considering its location, for the TEST set
devices_freqs_by_loc = []
counter = 1
for device_test in devices_test:
	print len(devices_test), counter
	df_device = events_test[ events_test["device_id"] == device_test ]
	device_freqs_by_loc = pd.DataFrame()

	for row in df_device.iterrows():
		row = row[1]
		lon = row["longitude"]
		lat = row["latitude"]

		nn_freqs = freq_df_by_loc[ (freq_df_by_loc["longitude"] == lon) & (freq_df_by_loc["latitude"] == lat) ]
		if (len(nn_freqs) > 0):
			device_freqs_by_loc = device_freqs_by_loc.append(nn_freqs, ignore_index=True)

	if (len(device_freqs_by_loc) > 0):
		summarized = summarize_fres_by_device(device_test, device_freqs_by_loc)
		devices_freqs_by_loc.append(summarized)
	counter = counter + 1

devices_fresq_test = pd.DataFrame(devices_freqs_by_loc)

devices_fresq_test.to_csv(data_dir + "devices_nn_location_test.csv")


#calculating the frequencies for each device, considering its location, for the TRAIN set
devices_freqs_by_loc_train = []
for device_train in devices:
	df_device = events[ events["device_id"] == device_train ]
	group = list(df_device["group"].drop_duplicates())[0]
	device_freqs_by_loc = pd.DataFrame()

	for row in df_device.iterrows():
		row = row[1]
		lon = row["longitude"]
		lat = row["latitude"]
		nn_freqs = freq_df_by_loc[ (freq_df_by_loc["longitude"] == lon) & (freq_df_by_loc["latitude"] == lat) ]
		if (len(nn_freqs) > 0):
			device_freqs_by_loc = device_freqs_by_loc.append(nn_freqs, ignore_index=True)

	if (len(device_freqs_by_loc) > 0):
		summarized = summarize_fres_by_device(device_train, device_freqs_by_loc, train_set=True, group=group)
		devices_freqs_by_loc_train.append(summarized)

devices_fresq_train = pd.DataFrame(devices_freqs_by_loc_train)

devices_fresq_train.to_csv(data_dir + "devices_nn_location_train.csv")





### TEST ###

#t = events[ (	 events["longitude"] >= 121.38) & 
#				(events["longitude"] <= 121.4 ) &
#				(events["latitude"]  >=  31.22) &
#				(events["latitude"]  <=  31.24)]
#del t["longitude"]
#del t["latitude"]
#t = t.drop_duplicates()


#t = events[ (	 events["longitude"] >= 104.05) & 
#				(events["longitude"] <= 104.07) &
#				(events["latitude"]  >=  30.64) &
#				(events["latitude"]  <=  30.66)]
#del t["latitude"]
#del t["longitude"]
#t = t.drop_duplicates()

