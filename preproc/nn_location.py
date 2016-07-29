import pandas as pd
from os import chdir
import gc
import sys
import numpy

working_dir = "/home/tales/development/kaggle-talking-data/"
data_dir = "data/"
chdir(working_dir)

wt_loc = pd.read_csv(data_dir + "wt_loc_group.csv", sep=";")

'''
Returns the boundaries of the nearests location neighbors.
args:
	loc_base: location center
	delta: the radius from the loc_base that defines its neighborhood
'''
def get_boundaries(loc_base, delta):
	loc_base_lon = loc_base[0]
	loc_base_lat = loc_base[1]
	delta_lon = loc_base_lon - (delta), loc_base_lon + (delta)
	delta_lat = loc_base_lat - (delta), loc_base_lat + (delta)
	return delta_lon, delta_lat

def set_wheight_delta(loc_base, df):
	loc_x = loc_base[0]
	loc_y = loc_base[1]
	df["neighbor_wheight"] = 1 / (numpy.sqrt((loc_x - df["lon"])**2 + (loc_y - df["lat"])**2))
	return df

loc_base = (86.15, 41.76)

delta_lon, delta_lat = get_boundaries(loc_base, 5)
print delta_lon, delta_lat

df = wt_loc[ (wt_loc["lon"] > delta_lon[0]) & (wt_loc["lon"] < delta_lon[1]) ]
print df

df = set_wheight_delta(loc_base, df)

df[["lon", "lat", "neighbor_wheight"]]

