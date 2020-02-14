import main
'''
Initializes the data environment and calls functions from main.py to 
do the modeling part.
'''

#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import pathlib

from scipy import stats
from fitter import Fitter
from os.path import join

curr_script_loc = pathlib.Path(__file__).parent.absolute()
input_file = join(curr_script_loc, '../input_data/Data.xlsx')
op_dir = join(curr_script_loc, '../output_data')
df = pd.read_excel(input_file)
dfc = df.copy()


def runpx(jobid, ip_file, op_dir):
    key_data, keys = main.builddf(dfc)  # Build a data frame according to the keys.
    dfs = key_data
    # Work with a particular data set.
    dfe = dfs[keys[100]]
    # Make sure the dataset is not too small so the model could be extended.
    print("Size of the data set: Rows = {} and columns = {}".format(dfe.shape[0], dfe.shape[1]))
    main.find_gradient(dfe)
    points_dim = main.podr_full(key_data, keys)

    with open(join(op_dir, 'results.txt'), 'w') as f:
        for key, value in points_dim.items():
            f.write('%s:%s\n' % (key, value))
    x_cord, y_cord = main.podr_x_y(points_dim)
    main.get_images(op_dir,dfe)
    # Build a data frame to analyze (x,y) values of point of diminishing returns.
    podrs = pd.DataFrame(list(zip(x_cord, y_cord)), columns=['podr_x', 'podr_y'])
    with open(join(op_dir, 'stats.txt'), 'a') as f3:
        print("Stats for x values \n", stats.describe(podrs['podr_x']), file=f3)
        print("Stats for y values \n", stats.describe(podrs['podr_y']), file=f3)
        # ds = podr_dist()
        # ds_num = ds.to_numpy()
        # f3.write(ds_num)


if __name__ == '__main__':
    runpx('jid',input_file, op_dir)

