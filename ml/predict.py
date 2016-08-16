import pandas as pd
from os import chdir
import gc
import sys
import numpy as np
sys.path.append("ml/libs/")
from BoosterXG import BoosterXG
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

data_dir = "data/"
prediction_dir = "ml/predictions/"
working_dir = "/home/tales/development/kaggle-talking-data/"
chdir(working_dir)

#### GET DATA READY ####
dtypes = {'device_id': str, 'gender': str, 'age': int, 'group': str, 'week_path_weight': float, 
'week_path_weight_by_days': float, 'weekend_path_weight': float, 'weekend_path_weight_by_days': float, 
'nn.F23-': float, 'nn.F24-26': float, 'nn.F27-28': float, 'nn.F29-32': float, 'nn.F33-42': float, 
'nn.F43+': float, 'nn.M22-': float, 'nn.M23-26': float, 'nn.M27-28': float, 'nn.M29-31': float, 
'nn.M32-38': float, 'nn.M39+': float, 'top_3_installed_apps': str, 'top_2_installed_apps': str, 
'top_1_installed_app': str, 'distinct_app_categories': float, 'distinct_active_app_categories': float, 
'top_2_active_apps': str, 'top_3_active_apps': str, 'top_1_active_app': str, 'cluster_12': str, 
'cluster_24': str, 'cluster_36': str, 'cluster_48': str, 'model_id': str, 'brand_id': str}

target = "group"

data_test = pd.read_csv(data_dir + "/data_test.csv", dtype=dtypes, sep=";") 
data_train = pd.read_csv(data_dir + "/data_train.csv", dtype=dtypes, sep=";")
del data_train['Unnamed: 0']
del data_train['gender']
del data_train['age']
del data_test['Unnamed: 0']

#this encoding replaces the categorical valuer with a number that xgboost uses as numeric
def dummy_encode(data):
	data.top_3_installed_apps = LabelEncoder().fit_transform(data.top_3_installed_apps)
	data.top_2_installed_apps = LabelEncoder().fit_transform(data.top_2_installed_apps)
	data.top_3_active_apps = LabelEncoder().fit_transform(data.top_3_active_apps)
	data.top_2_active_apps = LabelEncoder().fit_transform(data.top_2_active_apps)
	data.model_id = LabelEncoder().fit_transform(data.model_id)
	data.brand_id = LabelEncoder().fit_transform(data.brand_id)
	return data

data_train = dummy_encode(data_train)
data_test = dummy_encode(data_test)

def remove_categorical_columns(data):
	use_cols = []
	for col in data.columns.tolist():
		if(dtypes[col] != str or col == "device_id" or  col == target or col == "top_3_installed_apps" or col == "top_2_installed_apps" or col == "top_3_active_apps" or col == "top_2_active_apps" or col == "model_id" or col == "brand_id"):
			use_cols.append(col)
	print use_cols
	return data[use_cols]

data_test = remove_categorical_columns(data_test)
data_train = remove_categorical_columns(data_train)

def remove_other_columns(data, columns_to_remove):
	cols = data.columns.tolist()
	for col in columns_to_remove:
		cols.remove(col)
	return data[cols]

data_test = remove_other_columns(data_test, ['week_path_weight', 'weekend_path_weight'])
data_train = remove_other_columns(data_train, ['week_path_weight', 'weekend_path_weight'])

data_train["groupi"] = LabelEncoder().fit_transform(data_train.group)
data_train["groupi"] = data_train["groupi"]
groupi = data_train[["group", "groupi"]].drop_duplicates().sort("groupi")
del data_train["group"]
target = "groupi"

features = data_train.columns.tolist()
features.remove(target)

data_train = data_train.sort(columns="groupi")

#data_train = data_train.dropna(how="any")[features + [target]]
#data_test = data_test.dropna(how="any")[features]

########################

params = {}
params['max_depth'] = 8 #depth of decision tree, the higher it is increases the overfitting
params['bst:eta'] = 0.5 #makes the model more robust by shrinking the weights on each step
params['silent'] = 1 #feedback running prints
params['objective'] = "multi:softprob" #output a vector of ndata * nclass
params['nthread'] = 2 #number of parallel threads used to run xgboost
params['eval_metric'] = 'mlogloss' #multiclass logloss 
params['subsample'] = 0.75 #portion of data instances that XGBoost randomly collects to grow trees to prevent overfitting
params['colsample_bytree'] = 0.8 #subsample ratio of columns when constructing each tree
params['num_class'] = 12
num_boost_round = 400 #number of boosting iterations.
early_stopping_rounds = 50 # ??

bxg = BoosterXG(data_train, data_test, target, features, params, num_boost_round, early_stopping_rounds)

pred = bxg.run_xgboost()

score = bxg.cross_validation(test_size=0.25)
print score


def generate_submission(pred, devices_test, groupi):
	rows = []
	len_devices_test = len(devices_test)
	for index in range(len(devices_test)):
		print len_devices_test, index
		row = {}
		row["device_id"] = devices_test[index]
		for index_group in groupi["groupi"].tolist():
			mapping = groupi[groupi["groupi"] == index_group]["group"].item()
			row[mapping] = pred[index][index_group]
		rows.append(row)
	return pd.DataFrame(rows)

subm = generate_submission(pred, data_test.device_id.tolist(), groupi)

cols = subm.columns.tolist()
cols = cols[-1:] + cols[:-1]
subm = subm[cols]

len(subm)
subm = subm=drop_duplicates(subset=["device_id"])
len(subm)

subm.to_csv("ml/predictions/" + "subxg.csv", sep = ",", index=False)



