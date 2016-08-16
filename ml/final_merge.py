#script to merge datasets for machine learning

import pandas as pd
from os import chdir
import gc
import sys

def load_path_weight(dataset):
	path_weight_week = pd.read_csv(data_dir + "/path_weight_week.csv", dtype=dtypes, sep=",")
	path_weight_weekend = pd.read_csv(data_dir + "/path_weight_weekend.csv", dtype=dtypes, sep=",")
	#
	week_columns = path_weight_week.columns.tolist()
	week_columns[week_columns.index("path_weight")] = "week_path_weight"
	week_columns[week_columns.index("path_weight_by_days")] = "week_path_weight_by_days"
	path_weight_week.columns = week_columns
	del path_weight_week["Unnamed: 0"]
	#
	weekend_columns = path_weight_weekend.columns.tolist()
	weekend_columns[weekend_columns.index("path_weight")] = "weekend_path_weight"
	weekend_columns[weekend_columns.index("path_weight_by_days")] = "weekend_path_weight_by_days"
	path_weight_weekend.columns = weekend_columns
	del path_weight_weekend["Unnamed: 0"]
	#
	path_weight = pd.merge(path_weight_week, path_weight_weekend, on='device_id', how='outer')
	#
	if(dataset == "train"):
		data = pd.merge(devices_train, path_weight, on='device_id', how='inner')
		del data["group"]
		del data["gender"]
		del data["age"]
		return data
	#
	elif(dataset == "test"):
		data =  pd.merge(devices_test, path_weight, on='device_id', how='inner')
		return data
	#
	else:
		raise Exception("dataset argument must be 'train' or 'test'")

def load_nn_location(dataset):
	if (dataset == "train"):
		data = pd.read_csv(data_dir + "/devices_nn_location_train.csv", dtype=dtypes, sep=",")
		del data["group"]
		del data["Unnamed: 0"]
		return data
	elif (dataset == "test"):
		data = pd.read_csv(data_dir + "/devices_nn_location_test.csv", dtype=dtypes, sep=",")
		del data["Unnamed: 0"]
		return data

# Inserted by Henrique
def load_app_event_activity():
	data = pd.read_csv(data_dir + "/device_top_apps_prediction_ready.csv", dtype=dtypes, sep=";")
	return data

def load_app_usage_clusters(dataset, n):
	if (dataset == "train"):
		data = pd.read_csv(data_dir + "/app_cluster_" + str(n) + "_train.csv", dtype=dtypes, sep=";")
		del data["Unnamed: 0"]
		data.columns = ["device_id", "cluster_" + str(n)]
		return data
	elif (dataset == "test"):
		data = pd.read_csv(data_dir + "/app_cluster_" + str(n) + "_test.csv", dtype=dtypes, sep=";")
		del data["Unnamed: 0"]
		data.columns = ["device_id", "cluster_" + str(n)]
		return data

def get_brand_model():
	model_device = pd.read_csv(data_dir + "/model_device.csv", dtype=dtypes, sep=",")
	phone_brand = pd.read_csv(data_dir + "/phone_brand.csv", dtype=dtypes, sep=",")
	phone_brand_device_model = pd.read_csv(data_dir + "phone_brand_device_model.csv", dtype=dtypes, sep=",")
	#
	phone_brand_device_model = pd.merge(phone_brand_device_model, model_device, on='device_model', how='inner')
	phone_brand_device_model = pd.merge(phone_brand_device_model, phone_brand, on='phone_brand', how='inner')
	del phone_brand_device_model["phone_brand"]
	del phone_brand_device_model["device_model"]
	return phone_brand_device_model

def merge_all(df_list, dataset):
	if(dataset == "train"):
		devices = devices_train.drop_duplicates()
	elif(dataset == "test"):
		devices = devices_test.drop_duplicates()
	#
	final_df = devices
	#
	for df in df_list:
		final_df = pd.merge(final_df, df, on='device_id', how='left')
	#
	return final_df

data_dir = "data/"
working_dir = "/home/tales/development/kaggle-talking-data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": str, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}

devices_train = pd.read_csv(data_dir + "/gender_age_train.csv", dtype=dtypes, sep=",")
devices_test = pd.read_csv(data_dir + "/gender_age_test.csv", dtype=dtypes, sep=",")

phone_model_brand = get_brand_model()

pw_train = load_path_weight("train")
pw_test = load_path_weight("test")

nn_loc_train = load_nn_location("train")
nn_loc_test = load_nn_location("test")

device_app_activity = load_app_event_activity()

app_usage_cluster_train_12 = load_app_usage_clusters("train", 12)
app_usage_cluster_test_12 = load_app_usage_clusters("test", 12)

app_usage_cluster_train_24 = load_app_usage_clusters("train", 24)
app_usage_cluster_test_24 = load_app_usage_clusters("test", 24)

app_usage_cluster_train_36 = load_app_usage_clusters("train", 36)
app_usage_cluster_test_36 = load_app_usage_clusters("test", 36)

app_usage_cluster_train_48 = load_app_usage_clusters("train", 48)
app_usage_cluster_test_48 = load_app_usage_clusters("test", 48)

data_train = merge_all([pw_train, nn_loc_train, device_app_activity, app_usage_cluster_train_12, app_usage_cluster_train_24, app_usage_cluster_train_36, app_usage_cluster_train_48, phone_model_brand], "train")
data_test = merge_all([pw_test, nn_loc_test, device_app_activity, app_usage_cluster_test_12, app_usage_cluster_test_24, app_usage_cluster_test_36, app_usage_cluster_test_48, phone_model_brand], "test")

data_train.to_csv(data_dir + "data_train.csv", sep = ";")
data_test.to_csv(data_dir + "data_test.csv", sep = ";")
