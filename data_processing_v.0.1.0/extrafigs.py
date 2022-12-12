# file to produce some other plots for reference
# @oscar47

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import tqdm as tqdm
from scipy import optimize
from mpl_toolkits.axes_grid1 import make_axes_locatable

from mmgen2 import *
from lcgen import *

# set directory
MAIN_DIR = '/home/oscar47/Desktop/astro101/data/g_band'
DATA_DIR = os.path.join(MAIN_DIR, 'var_output/v0.1.1')
DATA_DIR2 = os.path.join(MAIN_DIR, 'var_output/v0.1.0')
LC_DIR = os.path.join(MAIN_DIR, 'g_band_lcs') # for folded .dats
LC_OUT = os.path.join(MAIN_DIR, 'sample_lcs')

# read csv
# = pd.read_csv(os.path.join(DATA_DIR, 'mm_2_n_targ_var.csv'))
#print(mm_n['name'].to_list())

# go through and divide df based on object name; use vars_unique from mmgen2
def get_var_unique():
    var_type_names = [] # list to hold the names of types of variables
    var_type_nums = [] # list to hold number of objects per class
    for var in var_unique:
        mm_type = mm_n.loc[mm_n['target']==var]
        names = mm_type['name'].to_list()
        var_type_names.append(names)
        var_type_nums.append(len(names))
    return var_type_names, var_type_nums

# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

# function to make histogram 
def make_hist():
    var_type_names, var_type_nums = get_var_unique()

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
    var_type_names, var_type_nums = get_var_unique()

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

# function tp plot our calculated periods vs theirs
def compare_periods(asassn, mm):
    # since rows of asassn dont match the order of mm, need to create new df
    combined_df = pd.DataFrame()
    id_list = []
    asassn_per_ls = []
    mm_per_ls = []
    for i in tqdm(range(len(mm)), position=0, desc='loading all variables...'):
        id = mm.iloc[i]['name'] # get name and our period
        # print(id)
        # print(type(id))
        mm_per = mm.iloc[i]['period']
        # now find the same row in asassn
        asassn_per = asassn.loc[asassn['ID']==id]['Period'].to_list()[0]
        # need to check for nan periods
        if not(asassn_per > 0):
            asassn_per = 0 # map nans to 0

        # print(asassn_per)
        # print(type(asassn_per))
        # print(asassn_per[0])
        # print(asassn_per[1])

        # now append to lists
        id_list.append(id)
        asassn_per_ls.append(asassn_per)
        mm_per_ls.append(mm_per)

        # print(asassn_per)
        # print(mm_per)

    # now put these into the df
    combined_df['namne'] = id_list
    combined_df['asassn per'] = asassn_per_ls
    combined_df['mm per'] = mm_per_ls

    print('saving!')

    combined_df.to_csv(os.path.join(MAIN_DIR, 'combined_period.csv'))

# compute Euclidean distance between all points in the two lists
def get_dist(ls1, ls2, epsilon):
    dist_ls = [] # initialize total list to hold number of points that are within epislon of that point
    for x in tqdm(ls1, position=0, desc='main loop...'):
        c = 0 # counter
        for y in ls2:
            if np.abs(x-y) <= epsilon:
                c+=1
        dist_ls.append(c)
    return dist_ls


def plot_per_compare(combined_df):
    asassn_per_ls = combined_df['asassn per'].to_list()
    mm_per_ls = combined_df['mm per'].to_list()

    plt.figure(figsize=(10, 7))
    plt.scatter(asassn_per_ls, mm_per_ls, color='blue', label='raw')

    # now let's do lin reg
    def func(x, a, b): # functopmn 
        y = a*x + b
        return y

    # fit the curve
    alpha = optimize.curve_fit(func, xdata = asassn_per_ls, ydata = mm_per_ls)[0]
    # need to define a linspace so we can plot continuous function
    x = np.linspace(min(asassn_per_ls), max(asassn_per_ls), 1000) # from min to max x with 1000 steps
    plt.plot(x, alpha[0]*x + alpha[1], color='red', label='y = %fx + %f'%(alpha[0], alpha[1]))

    # get R^2; see https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit for reference
    residuals = []
    for i ,x in enumerate(asassn_per_ls):
        y_pred = func(x, alpha[0], alpha[1])
        residual = mm_per_ls[i] - y_pred
        residuals.append(residual)
    residuals= np.array(residuals)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((mm_per_ls-np.mean(mm_per_ls))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # add other plot elements and then show
    plt.legend()
    plt.xlabel('ASAS-SN periods', fontsize=16)
    plt.ylabel('MM periods', fontsize=16)
    plt.title('Comparison of given vs calculated periods, $R^2=%f$'%np.round(r_squared, 4), fontsize=18)
    plt.show()

def plot_per_compare_dist(combined_df):
    asassn_per_ls = combined_df['asassn per'].to_list()
    mm_per_ls = combined_df['mm per'].to_list()
    c = combined_df['dist'].to_list()

    cmap = mpl.cm.viridis
    norm = mpl.colors.Normalize(vmin=min(c), vmax=max(c))

    fig, ax = plt.subplots()

    #ax.set_ylim(0, 1000) # to seee straight line

    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), label='Number of neighbors', ax=ax)
    #ax.figure(figsize=(10, 7))
    ax.scatter(asassn_per_ls, mm_per_ls, c=c, cmap=cmap, label='raw')

    # now let's do lin reg
    def func(x, a, b): # functopmn 
        y = a*x + b
        return y

    # fit the curve
    alpha = optimize.curve_fit(func, xdata = asassn_per_ls, ydata = mm_per_ls)[0]
    # need to define a linspace so we can plot continuous function
    x = np.linspace(min(asassn_per_ls), max(asassn_per_ls), 1000) # from min to max x with 1000 steps
    ax.plot(x, alpha[0]*x + alpha[1], color='red', label='y = %fx + %f'%(alpha[0], alpha[1]))

    # get R^2; see https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit for reference
    residuals = []
    for i ,x in enumerate(asassn_per_ls):
        y_pred = func(x, alpha[0], alpha[1])
        residual = mm_per_ls[i] - y_pred
        residuals.append(residual)
    residuals= np.array(residuals)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((mm_per_ls-np.mean(mm_per_ls))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # add other plot elements and then show
    ax.legend()
    ax.set_xlabel('ASAS-SN periods', fontsize=16)
    ax.set_ylabel('MM periods', fontsize=16)
    ax.set_title('Period plot for %.1f Random, $R^2=%.4f$'%(int(len(combined_df)), np.round(r_squared, 4)), fontsize=18)
    plt.show()
    

# comparing periods------------------------
# load in asassn and unnormalized mm
# asassn = pd.read_csv(os.path.join(MAIN_DIR, 'asassn_variables_x.csv'))
# mm = pd.read_csv(os.path.join(DATA_DIR2, 'mm_2_un.csv'))

# call function----------------------------
#compare_periods(asassn, mm)

# load in csv-------------
#combined_df = pd.read_csv(os.path.join(MAIN_DIR, 'combined_period.csv'))

# get distances
# want to calculate for small subset, ~5000
# combined_trim_df = pd.DataFrame({'asassn per': [], 'mm per': []})
# #combined_trim_df = pd.DataFrame()
# for i in tqdm(range(10000), desc='loading trim...'):
#     index = np.random.randint(0, len(combined_df))
#     #print(index)
#     combined_trim_df =combined_trim_df.append(combined_df.iloc[index], ignore_index=True)
#     #print(len(combined_trim_df))
# asassn_per_ls = combined_trim_df['asassn per'].to_list()
# mm_per_ls = combined_trim_df['mm per'].to_list()
# epsilon=0.5 # radius of similarity
# dist_ls = get_dist(asassn_per_ls, mm_per_ls, epsilon)
# combined_trim_df['dist']=dist_ls
# combined_trim_df.to_csv(os.path.join(MAIN_DIR, 'combined_trim_dist.csv'))


# plot_per_compare(combined_df)

# trying different restrictions on our distance dataset to investigate linear trend
combined_trim_df = pd.read_csv(os.path.join(MAIN_DIR, 'combined_trim_dist.csv'))
combined_trim_trim_df = combined_trim_df.loc[(combined_trim_df['mm per'] <= 1000) & (combined_trim_df['mm per'] > 10) & (combined_trim_df['asassn per'] > 10)] # get trimmed to see line more clearly
plot_per_compare_dist(combined_trim_trim_df)


#print(var_type_names)
#get_sample_lcs()

        