#this script generates the group count for the locations
#only to have insights

import pandas as pd
from os import chdir
import gc
import sys

def save_group_frequencies(df_groupby, gender_age_factors):
	rows = []
	#print df_groupby
	for group in df_groupby:
		#due to python way to represent decimals, it changes (a little bit) the number
		#rounding back to 2 decimals can fix this
		group_lon = round(group[0][0], 2)
		group_lat = round(group[0][1], 2)
		group_df = group[1]
		print group_df
		print 
		row = build_csv_rows(group_df, group_lon, group_lat, gender_age_factors)		

		rows.append(row)
	freq_df = pd.DataFrame(rows)
	freq_df.columns = ["lon", "lat", "F23-", "F24-26", "F27-28", "F29-32", "F33-42", "F43+", "M22-", "M23-26", "M27-28", "M29-31", "M32-38", "M39+", "total"]
	freq_df.to_csv(data_dir + "wt_loc_group.csv", index=False, sep=";")

#csv layout
#lon, lat, F23-, F24-26, F27-28, F29-32, F33-42, F43+, M22-, M23-26, M27-28, M29-31, M32-38, M39+, total
def build_csv_rows(group_df, group_lon, group_lat, gender_age_factors):
	row = [group_lon, group_lat]
	n_ocurrences = len(group_df)
	freq = dict(group_df.group.value_counts())
	for ga in gender_age_factors:
		if(ga in freq.keys()):
			#print ga, "\t", freq[ga]
			row.append(freq[ga])
		else:
			#print ga, "\t", 0
			row.append(0)
	row.append(n_ocurrences)
	#print n_ocurrences
	return row

#working_dir = sys.argv[1]
#data_dir = sys.argv[2]
#dataset = sys.argv[3]

working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"
dataset = "train"

chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}

events = pd.read_csv(data_dir + "/events_v2.csv", dtype=dtypes, sep=";")

if (dataset == "train"):
	gender_age = pd.read_csv("data/gender_age_train.csv", dtype=dtypes)
	del gender_age['gender']
	del gender_age['age']
elif (dataset == "test"):
	gender_age = pd.read_csv("data/gender_age_test.csv", dtype=dtypes)
else:
	raise Exception("You mus specify a dataset to build: train or test")

gender_age_factors = list(gender_age.group.drop_duplicates().sort_values())

gc.collect()
events = pd.merge(events, gender_age, on='device_id', how='inner')
events.head()
len(events)
gender_age = None
gc.collect()

#keep workdays
events = events[(events["weekday"] != "saturday") & (events["weekday"] != "sunday")]

#keep work daytimes
events = events[(events["daytime"] == "morning") | (events["daytime"] == "afternoon")]

del events['timestamp']
del events['event_id']
del events['weekday']
del events['daytime']
#del events['device_id']
gc.collect()

events = events.drop_duplicates()
events.head()

grouped_by_loc = events.groupby(["longitude", "latitude"])

save_group_frequencies(grouped_by_loc, gender_age_factors)