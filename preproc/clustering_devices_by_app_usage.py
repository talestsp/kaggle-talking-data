import pandas as pd
from os import chdir
import gc
from sklearn import KMeans

working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}
from sklearn import KMeans
data_train = pd.read_csv(data_dir + "/device_apps_freq_train.csv", dtype=dtypes, sep=";")
data_test = pd.read_csv(data_dir + "/device_apps_freq_test.csv", dtype=dtypes, sep=";")

data = pd.concat([data_train, data_test])

KMeans(n_clusters=12, max_iter=1000)
