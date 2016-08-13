import pandas as pd
from os import chdir
import gc
from sklearn.cluster import KMeans

working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"
chdir(working_dir)

n = 48

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}

data_train = pd.read_csv(data_dir + "/device_apps_freq_train.csv", dtype=dtypes, sep=";")
data_test = pd.read_csv(data_dir + "/device_apps_freq_test.csv", dtype=dtypes, sep=";")

data = pd.concat([data_train, data_test])
data.head()
keys = data["device_id"]
keys.head()
del data["device_id"]
del data["Unnamed: 0"]

km = KMeans(n_clusters=n, max_iter=1000, init="k-means++")
km.fit(data)

data_clusters = pd.DataFrame()
data_clusters["device_id"] = keys
data_clusters["cluster"] = km.labels_

data_clusters.head()

train = data_clusters[data_clusters.device_id.isin(data_train.device_id.tolist())]
test = data_clusters[data_clusters.device_id.isin(data_test.device_id.tolist())]

train.to_csv(data_dir + "app_cluster_" + str(n) + "_train.csv", sep = ";")
test.to_csv(data_dir + "app_cluster_" + str(n) + "_test.csv", sep = ";")