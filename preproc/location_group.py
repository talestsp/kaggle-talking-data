#Script to group (gender, age) by location (longitude, latidude)
#Note that 2 decimal numbers at coordinates separates 1,1km

#Maybe try to group also by timestamp (rounding?)

import pandas as pd
from os import chdir
import gc

def save_group_frequencies(df_groupby, gender_age_factors):
	rows = []
	for group in df_groupby:
		#due to python way to represent decimals, it changes (a little bit) the number
		#rounding back to 2 decimals can fix this
		group_lon = round(group[0][0], 2)
		group_lat = round(group[0][1], 2)
		group_df = group[1]

		print group_lon, group_lat
		print group_df
		
		row = build_csv_rows(group_df, group_lon, group_lat, gender_age_factors)
		
		print row
		print "---"
		print
		
		rows.append(row)

	freq_df = pd.DataFrame(rows)
	freq_df.columns = ["lon", "lat", "F23-", "F24-26", "F27-28", "F29-32", "F33-42", "F43+", "M22-", "M23-26", "M27-28", "M29-31", "M32-38", "M39+", "total"]
	freq_df.to_csv("data/location_group.csv", index=False, sep=";")

#csv layout
#lon, lat, F23-, F24-26, F27-28, F29-32, F33-42, F43+, M22-, M23-26, M27-28, M29-31, M32-38, M39+, total
def build_csv_rows(group_df, group_lon, group_lat, gender_age_factors):
	row = [group_lon, group_lat]
	n_ocurrences = len(group_df)
	freq = dict(group_df.group.value_counts())
	
	for ga in gender_age_factors:
	
		if(ga in freq.keys()):
			print ga, "\t", freq[ga]
			row.append(freq[ga])
	
		else:
			print ga, "\t", 0
			row.append(0)
	
	row.append(n_ocurrences)
	print n_ocurrences
	return row

working_dir = "/home/tales/development/kaggle-talking-data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str}

events = pd.read_csv("data/events.csv", dtype=dtypes)
len(events)
events.head()
gender_age = pd.read_csv("data/gender_age_train.csv", dtype=dtypes)
gender_age_factors = list(gender_age.group.drop_duplicates().sort_values())
len(gender_age)
gender_age.head()

group_loc = pd.merge(gender_age, events, on='device_id', how='left')
del group_loc['event_id']
events = None
gender_age = None
gc.collect()

grouped_by_loc = group_loc.groupby(["longitude", "latitude"])

save_group_frequencies(grouped_by_loc, gender_age_factors)

#Henrique, if you check this out you'll see how amazing this featrue could be!! :D
#Result: csv with group (gender-age) frequencies and can be used to get frequencies of neighbors location, example (12.34, 11.11) is in (12.33, 11.11) neighborhood 

