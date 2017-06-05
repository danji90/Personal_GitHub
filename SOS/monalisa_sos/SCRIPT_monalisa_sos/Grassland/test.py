import numpy as np
import os

data_folder = 'C:/monalisa_sos/DATA_monalisa_sos/Grassland/'

data_folder_entries = os.listdir(data_folder)

stations = []
for r in range(0, len(data_folder_entries)):
    if os.path.isdir(data_folder + data_folder_entries[r]):
        stations.append(data_folder_entries[r])
    else:
        continue

dirs = []
NaN_rem = '_NaNremoved'

for o in range(0, len(stations)):
     dirs.append(data_folder + stations[o] + '/' + stations[o] + NaN_rem + '/')


files = os.listdir(dirs)

file = dirs + files

with open(file, 'r') as f:
    lines = f.readlines()
    num_cols = len(lines[0].split(','))
f.close()

values = np.loadtxt(file, delimiter=',', usecols=range(1, num_cols))