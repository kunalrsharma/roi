
'''
This file takes the raw data which is in the form {(x,y,key)}
where 'key': Ad-campaign,
 x: price
 y: return on investment.

 The goal here is to find the point of diminishing returns for
 each Ad-campaign.
 As point of diminishing returns is defined as point where the
 marginal increase starts decreasing, we calculate the point
 where the second derivative of y as a function of x changes sign.

 The above is calculated for every campaign and proceeds by first
 smoothening the signal.
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

def builddf(data):
    '''
    This function organizes the data according to the keys.
    It builds a dictionary of the form (key, dataframe).
    '''
    keys = data['Key'].unique()
    print("The number of unique keys is: ", len(keys))
    key_data = {} # Build a dictionary
    for i,k in enumerate(keys):
        key_data[k] = data[data['Key']==k] # Datafrmae corresponding to the key.
    keys = keys.tolist()
    return (key_data, keys)

# Find the points of diminishing return
# To take the derivative of y with respect to x, we
# set the differential in x to '0.01' which is constant
# through out the data set.

def find_gradient(data):
    # Set the differential value
    dx = 0.01
    # Using numpy's 'gradient' to find the finite-difference (derivative).
    y_1 = np.gradient(data['y'], dx)  # first derivative.
    data['y_1'] = y_1
    y_2 = np.gradient(data['y_1'], dx)  # second derivative.
    data['y_2'] = y_2


def savgol_f(data):
    '''Apply the filter with window size 51 and polynomial degree 1. '''
    # We smoothen the data three time whcih in our analysis makes
    # the data sufficently smooth.
    # Results of the data are stored in 'ys'
    window = 0
    if data.shape[0] < 50:
        window = 3
    elif 50<= data.shape[0] < 500:
        window = 11
    else:
        window = 51
    data['ys1']= savgol_filter(data['y'].values, window, 1)
    data['ys2']= savgol_filter(data['ys1'].values, window, 1)
    data['ys3']= savgol_filter(data['ys2'].values, window, 1)


# Now finding the point of diminishing returns.
# For that firstly we compute the derivatives.
def podr(data):
    # Calculate the derivatives first.
    dx = 0.01  # Set the differntial in x.
    first = np.gradient(data['ys3'], dx)
    data['first'] = first
    second = np.gradient(data['first'], dx)
    data['second'] = second
    # Calculate the point of diminishing returns.
    inf = []
    ps = 0
    std_unb = data['second'].std() / np.sqrt(data.shape[0])  # Calculate unbiased standard deviation.
    cut_off = int(0.5 * std_unb)  # Take half of it as cutoff.
    for i in range(data.shape[0]):
        if ((data['second'].iloc[-i] < 0) == False) and (data['second'].iloc[-i] > cut_off):
            inf.append((data.iloc[-1 - i, 1], data.iloc[-1 - i, 2]))  # Add (x,y) values.
    # Return the first point where the "If" condition above is satisfied.
    if len(inf) == 0:
        return -1
    else:
        return inf[0]


# Program to find the point of moving average for the whole data set.

# Corresponding to each key, we find the point of diminishing return,
# whcih is then returned by the function.

def podr_full(key_data, keys):
    points = {}
    for k in keys:
        data = key_data[k]  # Get the dataframe corresponding to the key.
        savgol_f(data) # Apply the filter to smoothen the data
        pts = podr(data) # Collect the points of diminishing returns.
        points[k] = pts
    return points


def get_images(op_dir,dfe):
    # Comparison of y value plots with and without smoothing.

    plt.subplot(1, 2, 1)
    plt.xlim(0, 50)  # Restricting x-vlaues for the above reason.
    plt.ylim(0, 100)  # Restricting y-values as standard deviation is small.
    plt.title('Plot of X-Y values before smoothing')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(dfe['x'], dfe['y'])

    plt.subplot(1, 2, 2)
    plt.title("X-Y values after smoothing")
    plt.xlim(0, 40)
    plt.ylim(0, 100)
    plt.ylabel("ys3")
    plt.xlabel("x")
    plt.plot(dfe['x'], dfe['ys3'])

    plt.tight_layout()
    plt.savefig(join(op_dir, 'plots.png'))

def podr_x_y(pts):
    x_val = [] # x coordinate of podr
    y_val = [] # y coordinate of podr
    vals = list(pts.values())
    vals.remove(-1)  # Remove an null value from the list to prevent errors.
    for v in vals:
        x_val.append(v[0])
        y_val.append(v[1])
    return x_val, y_val

def podr_dist():
    '''
    Input: X-vaules of the points of diminishing returns
    Output: Estimate of probability distribution of the input.
    '''
    #%% capture
    x_1 = podrs[podrs['podr_x'] < 17]
    fitt = Fitter(x_1['podr_x'])
    fitt.fit()
    with open(join(op_dir, 'distribution'), 'a') as f:
        print("The best distribution fit is: \n", fitt.get_best(),file=f)
        dist_sum = fitt.summary()
        print(dist_sum)
        dist = dist_sum.keys()
        #fitt.plot_pdf(dist)
        #sns.distplot(x_1['podr_x'])
    f.close()


