import pandas as pd
from os import chdir
#from ml.libs.XGBooster import XGBooster
import gc
import sys
sys.path.append("ml/libs/")
from BoosterXG import BoosterXG

data_dir = "data/"
prediction_dir = "ml/predictions/"
working_dir = "/home/tales/development/kaggle-talking-data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}

data_test = pd.read_csv(data_dir + "/data_test.csv", dtype=dtypes, sep=";")
data_train = pd.read_csv(data_dir + "/data_train.csv", dtype=dtypes, sep=";")




params = {}
params['bst:max_depth'] = 5 #depth of decision tree, the higher it is increases the overfitting
params['bst:eta'] = 0.2 = #makes the model more robust by shrinking the weights on each step
params['silent'] = 0 #feedback running prints
params['objective'] = "multi:softprob" #output a vector of ndata * nclass
params['nthread'] = 2 #number of parallel threads used to run xgboost
params['eval_metric'] = 'mlogloss' #multiclass logloss 
params['subsample'] = 0.65 #portion of data instances that XGBoost randomly collects to grow trees to prevent overfitting
params['colsample_bytree'] = 0.8 #subsample ratio of columns when constructing each tree
params['n_class'] = 12

num_boost_round = 500 #number of boosting iterations.
early_stopping_rounds = 50 #


