import pandas as pd
from os import chdir
import gc
import sys
import numpy as np
sys.path.append("ml/libs/")
from BoosterXG import BoosterXG

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

def remove_categorical_columns(data):
	use_cols = []
	for col in data.columns.tolist():
		if(dtypes[col] != str or col == target):
			use_cols.append(col)
	return data[use_cols]

def remove_other_columns(data, columns_to_remove):
	cols = data.columns.tolist()
	for col in columns_to_remove:
		cols.remove(col)
	return data[cols]


data_test = remove_categorical_columns(data_test)
data_train = remove_categorical_columns(data_train)

data_test = remove_other_columns(data_test, ['week_path_weight', 'weekend_path_weight'])
data_train = remove_other_columns(data_train, ['week_path_weight', 'weekend_path_weight'])

#features = ['group', 'week_path_weight', 'week_path_weight_by_days', 'weekend_path_weight', 'weekend_path_weight_by_days', 'nn.F23-', 'nn.F24-26', 'nn.F27-28', 'nn.F29-32', 'nn.F33-42', 'nn.F43+', 'nn.M22-', 'nn.M23-26', 'nn.M27-28', 'nn.M29-31', 'nn.M32-38', 'nn.M39+', 'top_3_installed_apps', 'top_2_installed_apps', 'top_1_installed_app', 'distinct_app_categories', 'distinct_active_app_categories', 'top_2_active_apps', 'top_3_active_apps', 'top_1_active_app', 'cluster_12', 'cluster_24', 'cluster_36', 'cluster_48', 'model_id', 'brand_id']
features = data_train.columns.tolist()
features.remove(target)

data_train = data_train.dropna(how="any")[features + [target]]
#data_test = data_test.dropna(how="any")[features]

########################

params = {}
params['bst:max_depth'] = 5 #depth of decision tree, the higher it is increases the overfitting
params['bst:eta'] = 0.2 #makes the model more robust by shrinking the weights on each step
params['silent'] = 1 #feedback running prints
params['objective'] = "multi:softprob" #output a vector of ndata * nclass
params['nthread'] = 2 #number of parallel threads used to run xgboost
params['eval_metric'] = 'mlogloss' #multiclass logloss 
params['subsample'] = 0.65 #portion of data instances that XGBoost randomly collects to grow trees to prevent overfitting
params['colsample_bytree'] = 0.8 #subsample ratio of columns when constructing each tree
params['num_class'] = 12
num_boost_round = 500 #number of boosting iterations.
early_stopping_rounds = 50 # ??

bxg = BoosterXG(data_train, data_test, target, features, params, num_boost_round, early_stopping_rounds)

#pred = bxg.run_xgboost()

score = bxg.cross_validation()
print score


