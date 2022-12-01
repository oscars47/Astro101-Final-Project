# file to produce some other plots for reference
# @oscar47

import os
import pandas as pd
import matplotlib.pyplot as plt
import tqdm as tqdm

from mmgen2 import *
from lcgen import *

# set directory
MAIN_DIR = '/home/oscar47/Desktop/astro101/data/g_band'
DATA_DIR = os.path.join(MAIN_DIR, 'var_output/v0.1.1')
LC_DIR = os.path.join(MAIN_DIR, 'g_band_lcs') # for folded .dats
LC_OUT = os.path.join(MAIN_DIR, 'sample_lcs')

# read csv
mm_n = pd.read_csv(os.path.join(DATA_DIR, 'mm_2_n_targ_var.csv'))
#print(mm_n['name'].to_list())

# go through and divide df based on object name; use vars_unique from mmgen2
var_type_names = [] # list to hold the names of types of variables
var_type_nums = [] # list to hold number of objects per class
for var in var_unique:
    mm_type = mm_n.loc[mm_n['target']==var]
    names = mm_type['name'].to_list()
    var_type_names.append(names)
    var_type_nums.append(len(names))

# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

# function to make histogram 
def make_hist():
    plt.figure(figsize=(10, 7))
    plt.bar(x=var_unique, height=var_type_nums, color='magenta')
    addlabels(var_unique, var_type_nums)
    plt.title('Number of objects per class', fontsize=18)
    plt.xlabel('Class', fontsize=16)
    plt.ylabel('Number of objects', fontsize=16)
    plt.show()

#make_hist(var_type_nums)

# functions to plot lcs for each class
def get_sample_lcs():
    for i in tqdm(range(len(var_unique))):
        var = var_unique[i]
        # make sub directory for each class
        # print(os.path.join(LC_OUT, var))
        # print(os.path.isdir(os.path.join(LC_OUT, var)))
        if not(os.path.isdir(os.path.join(LC_OUT, var))):
            print('making path!')
            os.makedirs(os.path.join(LC_OUT, var))
        # check if >= 5 lcs
        print(var_type_nums)
        if var_type_nums[i] >= 5:
            for j in range(5): # get 5 random indices
                index = int(var_type_nums[i]*np.random.random())
                name = var_type_names[i][index]
                file = get_file(name)
                target = mm_n.loc[mm_n['name']==name]['target'].to_list()[0]
                period = mm_n.loc[mm_n['name']==name]['period'].to_list()[0]
                get_lc(file, name, target, LC_DIR, os.path.join(LC_OUT, var))
                get_lc_fold(file, name, target, LC_DIR, os.path.join(LC_OUT, var), period)
        else:
            for j in range(len(var_type_names[i])):
                name = var_type_names[i][j]
                file = get_file(name)
                target = mm_n.loc[mm_n['name']==name]['target'].to_list()[0]
                period = mm_n.loc[mm_n['name']==name]['period'].to_list()[0]
                get_lc(file, name, target, LC_DIR, os.path.join(LC_OUT, var))
                get_lc_fold(file, name, target, LC_DIR, os.path.join(LC_OUT, var), period)
#print(var_type_names)
get_sample_lcs()

        