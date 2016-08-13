import pandas as pd
from os import chdir
import gc
import sys

data_dir = "data/"
prediction_dir = "ml/predictions/"
working_dir = "/home/tales/development/kaggle-talking-data/"
chdir(working_dir)

dtypes = {'label_id': int, 'category': str, "event_id": str, "device_id": str, "app_id": long, "is_installed": str,  "is_active": str, "gender": str ,"age": int, "group": str, "group": str, "phone_brand": str, "device_model": str, "daytime": str, "weekday": str}

data_test = pd.read_csv(data_dir + "/data_test.csv", dtype=dtypes, sep=";")

prediction = "00bc3d632c94"
pred = pd.read_csv(prediction_dir + prediction + ".csv", dtype=dtypes, sep=",")
del pred["predict"]

def format_solution():
	solution = pd.DataFrame(data_test.device_id)
	for col in pred.columns.tolist():
		solution[col] = pred[col].round(4)
	solution = solution.drop_duplicates(subset="device_id", keep="first")
	return solution

solution = format_solution()

solution.to_csv(prediction_dir + "solution-" +prediction + ".csv", sep = ",", index=False)
