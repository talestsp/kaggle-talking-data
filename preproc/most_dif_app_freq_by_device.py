#calculate the relative frequency of the most_diff apps usage by device_id
import pandas as pd
from os import chdir
import gc

working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"
chdir(working_dir)
dataset = "test"

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}

app_events = pd.read_csv(data_dir + "/app_events.csv", dtype=dtypes)
del app_events["is_installed"]
del app_events["is_active"]
gc.collect()

if dataset == "train":
	gender_age = pd.read_csv(data_dir + "/gender_age_train.csv", dtype=dtypes)
	del gender_age["gender"]
	del gender_age["age"]
	del gender_age["group"]
	gc.collect()
elif dataset == "test":
	gender_age = pd.read_csv(data_dir + "/gender_age_test.csv", dtype=dtypes)

events = pd.read_csv(data_dir + "/events.csv", dtype=dtypes)
del events["timestamp"]
del events["longitude"]
del events["latitude"]
gc.collect()

app_events = pd.merge(app_events, events, on='event_id', how='inner')
events = None
gc.collect()
app_events = pd.merge(app_events, gender_age, on='device_id', how='inner')

most_diff_apps = pd.read_csv(data_dir + "/most_diff_apps.csv", dtype=dtypes, sep=";")
most_diff_apps = most_diff_apps.head(10)
app_events = app_events[ app_events.app_id.isin(most_diff_apps.app_id) ].drop_duplicates()

app_events.head()

def top_freq(column):
	return column.value_counts()

freq_app_by_device = app_events.groupby(by="device_id")["app_id"].apply(top_freq)
freq_app_by_device.head()
count_events_by_device = app_events[["device_id", "event_id"]].drop_duplicates().device_id.value_counts()
count_events_by_device.head()

def build_df(freq_app_event, count_events):
	rows_freq_app = []
	for item in freq_app_event.iteritems():
		row_dict = {"device_id": item[0][0], "app_id": item[0][1], "freq": item[1]}
		rows_freq_app.append(row_dict)
	freq_app_event = pd.DataFrame(rows_freq_app)
	#
	rows_count_events = []
	for item in count_events.iteritems():
		row_dict = {"device_id": item[0], "count": item[1]}
		rows_count_events.append(row_dict)
	rows_count_events = pd.DataFrame(rows_count_events)
	#
	data = pd.merge(freq_app_event, rows_count_events, on='device_id', how='inner')
	data["freq_rel"] = data["freq"] / data["count"]
	data = data.sort(columns=["app_id", "device_id"])
	return data


#falta formatar, colocar colunas: device, app1, app2, app3
app_usage_by_device = build_df(freq_app_by_device, count_events_by_device)
def format_df_freq(df):
	device_ids_list = app_events.device_id.drop_duplicates().tolist()
	most_diff_apps_list = most_diff_apps.app_id.drop_duplicates().tolist()
	#
	rows = []
	for device_id in device_ids_list:
		device_df = df[df.device_id == device_id]
		device_row = {"device_id": device_id}
		for app_id in most_diff_apps_list:
			if(app_id in device_df.app_id.tolist()):
				device_row["freq_" + str(app_id)] = device_df[device_df.app_id == app_id].freq_rel.item()
			else:
				device_row["freq_" + str(app_id)] = 0
		rows.append(device_row)
	return pd.DataFrame(rows)

device_apps_freq = format_df_freq(app_usage_by_device)

if dataset == "train":
	device_apps_freq.to_csv(data_dir + "device_apps_freq_train.csv", sep = ";")
elif dataset == "test":
	device_apps_freq.to_csv(data_dir + "device_apps_freq_test.csv", sep = ";")