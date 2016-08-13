#analyze the common apps to all groups
#find the most diffent app on usage frequency
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

gender_age = pd.read_csv(data_dir + "/gender_age_train.csv", dtype=dtypes)
del gender_age["gender"]
del gender_age["age"]
gc.collect()

events = pd.read_csv(data_dir + "/events.csv", dtype=dtypes)
del events["timestamp"]
del events["longitude"]
del events["latitude"]
gc.collect()

app_events = pd.merge(app_events, events, on='event_id', how='inner')
events = None
gc.collect()
app_events = pd.merge(app_events, gender_age, on='device_id', how='inner')

app_events.head()

def n_events(column):
	return len(column)

def build_df(freq_app_event, count_events):
	rows_freq_app = []
	for item in freq_app_event.iteritems():
		row_dict = {"group": item[0][0], "app_id": item[0][1], "freq": item[1]}
		rows_freq_app.append(row_dict)
	freq_app_event = pd.DataFrame(rows_freq_app)
	#
	rows_count_events = []
	for item in count_events.iteritems():
		row_dict = {"group": item[0], "count": item[1]}
		rows_count_events.append(row_dict)
	rows_count_events = pd.DataFrame(rows_count_events)
	#
	data = pd.merge(freq_app_event, rows_count_events, on='group', how='inner')
	data["freq_rel"] = data["freq"] / data["count"]
	data = data.sort(columns=["app_id", "group"])
	return data

##################################
############ ANALYSIS ############
def top_freq(column, n=3):
	return column.value_counts().head(n)

freq_app_event_by_group = app_events.groupby(by="group")["app_id"].apply(top_freq)
count_events_by_group = app_events[["device_id", "event_id", "group"]].drop_duplicates().group.value_counts()

freq_app_event_by_group = build_df(freq_app_event_by_group, count_events_by_group)
count_events_by_group = None
gc.collect()

def compare_gender_app():
	compare_gender = [('F23-', 'M22-'), ('F24-26', 'M23-26'), ('F27-28', 'M27-28'), ('F29-32', 'M29-31'), ('F33-42', 'M32-38'), ('F43+', 'M39+')]
	for app_id in freq_app_event_by_group.app_id.drop_duplicates():
		use_df = freq_app_event_by_group[freq_app_event_by_group.app_id == app_id]
		for c in compare_gender:
			print use_df[(use_df.group == c[0]) | (use_df.group == c[1])]
		print use_df
		print use_df.freq_rel.std()
		print

compare_gender_app()
##################################

count_events_by_group = app_events[["device_id", "event_id", "group"]].drop_duplicates().group.value_counts()

###################################################
#####DISCOVER MOST DIFFERENT APPS ON USAGE RATE####
def top_freq(column, n=100):
	return column.value_counts().head(n)

freq_app_event_by_group = app_events.groupby(by="group")["app_id"].apply(top_freq)

freq_app_event_by_group = build_df(freq_app_event_by_group, count_events_by_group)

#freq_app_event_by_group["freq_abs"] = freq_app_event_by_group["freq"] / freq_app_event_by_group["count"]
#freq_app_event_by_group = freq_app_event_by_group.sort(columns=["app_id", "group"])

def get_most_different_apps():
	rows = []
	for app_id in freq_app_event_by_group.app_id.drop_duplicates():
		use_df = freq_app_event_by_group[freq_app_event_by_group.app_id == app_id]
		if len(use_df) == 12:
			rows.append({"app_id": app_id, "std": use_df.freq_rel.std()})
	return pd.DataFrame(rows)

most_diff_apps = get_most_different_apps().sort(columns="std", ascending=False)
most_diff_apps

app_1st_diff = app_events[app_events["app_id"] == 3433289601737013244]
app_1st_diff_freq = app_1st_diff.groupby(by="group").app_id.value_counts()
build_df(app_1st_diff_freq, count_events_by_group)

app_last_diff = app_events[app_events["app_id"] == -5301777493006977660]
app_last_diff_freq = app_last_diff.groupby(by="group").app_id.value_counts()
build_df(app_last_diff_freq, count_events_by_group)
###################################################

#########################################
###### CHECKING DIFF APPS COVERAGE ######
def check_coverage():
	cov_events = app_events[ app_events.app_id.isin(most_diff_apps.app_id.tolist()) ]
	devices_covered = cov_events.device_id.drop_duplicates()
	print len(devices_covered)
	print len(gender_age.device_id.drop_duplicates())
	return len(devices_covered) / float(len(gender_age.device_id.drop_duplicates()))

check_coverage()

most_diff_apps.to_csv(data_dir + "most_diff_apps.csv", sep = ";")
len(most_diff_apps)
#########################################


#TODO set the mode of those event_sizes by device 
#event_size_by_device = app_events.groupby(by=["device_id", "event_id"]).apply(n_events)
#event_size_by_device.to_csv(data_dir + "event_size_by_device.csv", sep = ";")



