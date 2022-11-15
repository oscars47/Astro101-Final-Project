# file to generate the monster matrix (mm) of var indices data for each lc object
# by @oscars47 and @ghirsch123

import os
from tqdm import tqdm
import pandas as pd
import numpy as np
# import files we've created
from lcgen import get_lc
from vargen import Variable

DATA_DIR = '/home/oscar47/Desktop/astro101/data/g_band'
LC_DIR = os.path.join(DATA_DIR, 'g_band_lcs')
LC_OUT = os.path.join(DATA_DIR, 'lc_output')
VAR_OUT = os.path.join(DATA_DIR, 'var_output')
FOLD_DIR = os.path.join(DATA_DIR, 'folded_g_band_lcs') # for folded .dats
FOLD_OUT = os.path.join(LC_OUT, 'folded')
IRREG_DIR = os.path.join(DATA_DIR, 'irreg_g_band_lc')

# confirm we have each of these directories
if not(os.path.isdir(DATA_DIR)):
    os.makedirs(DATA_DIR)
if not(os.path.isdir(LC_DIR)):
    os.makedirs(LC_DIR)
if not(os.path.isdir(LC_OUT)):
    os.makedirs(LC_OUT)
if not(os.path.isdir(VAR_OUT)):
    os.makedirs(VAR_OUT)
if not(os.path.isdir(FOLD_OUT)):
    os.makedirs(FOLD_OUT)
if not(os.path.isdir(FOLD_DIR)):
    os.makedirs(FOLD_DIR)
if not(os.path.isdir(IRREG_DIR)):
    os.makedirs(IRREG_DIR) 
# make list of all LC_DIR files
lc_files = os.listdir(LC_DIR)

# to get the names, first split by '.dat' and remove final element (.dat), recombine; then split based on '_' and replace with ' '
lc_names = []
for lc in lc_files:
    temp_list=[]
    temp_name = ''
    temp_list = lc.split('.dat')
    temp_name = temp_list[0]
    temp_list = temp_name.split('_')
    temp_name = temp_list[0] +' ' + temp_list[1]
    lc_names.append(temp_name)

# get unique classes of variable objects---------------
vars = pd.read_csv(os.path.join(DATA_DIR, 'asassn_variables_x.csv'))
var_unique = list(vars['ML_classification'].unique())

# fold lcs!-----------------------
# to be run once
def fold_lcs():
    for i in tqdm(range(len(lc_files)), desc='progress...', position=0, leave=True):
        name = lc_names[i]
        file = lc_files[i]
        # extract periods
        period = vars.loc[vars['ID']==name]['Period'].to_list()[0]
        
        # read in df
        c_path = os.path.join(LC_DIR, file)
        lc_df = pd.read_csv(c_path, sep='\t')

        # we need to extract the time list and mod each by the period
        time = np.array(lc_df['HJD'].to_list())
        #print(period, type(period))
        
        if (period > 0):
            time = time % period
            # now set the time column of df equal to this
            lc_df['HJD'] = time

            #now save lc_df as .dat in FOLD_DIR
            lc_df.to_csv(os.path.join(FOLD_DIR, file), sep='\t')
        else:
            lc_df.to_csv(os.path.join(IRREG_DIR, file), sep='\t')

        
#print(vars['Period'].to_list())
fold_lcs() # call to generate new .dats


# # for testing, let's get HADS, RVA-------------
# hads = vars.loc[vars['ML_classification']=='HADS']['ID'].to_list()
# ea = vars.loc[vars['ML_classification']=='EA']['ID'].to_list()

# # just take first 10
# ea = ea[:10]
# print(ea)

def get_file(name):
    temp_list = []
    temp_file = ''
    temp_list = name.split(' ')
    temp_file += temp_list[0] +'_' + temp_list[1] +'.dat'
    return temp_file

def get_name(file):
    temp_list=[]
    temp_name = ''
    temp_list = file.split('.dat')
    temp_name = temp_list[0]
    temp_list = temp_name.split('_')
    temp_name = temp_list[0] +' ' + temp_list[1]
    return temp_name

    
# get folded lcs
def get_first_fold_lc():
    for file in os.listdir(FOLD_DIR):
        name = get_name(file)
        get_lc(file, name, FOLD_DIR, FOLD_OUT)
    # compare to non-folded
    for i in range(5):
        file = lc_files[i]
        name = get_name(file)
        get_lc(file, name, LC_DIR, LC_OUT)


# # function to take in id and cleanup name to get lc--------------------
# def get_data(df, name):
#     temp_list = []
#     temp_file = ''
#     temp_list = name.split(' ')
#     temp_file += temp_list[0] +'_' + temp_list[1] +'.dat'

#     #get_lc(temp_file, name, LC_DIR, LC_OUT)
#     # create new instance of Variable object
#     temp_var = Variable(temp_file, name, LC_DIR)
#     df = df.append(temp_var.return_dict(), ignore_index=True)
#     return df

# # create new df --- the monster matrix --- to hold results of Variable obj
# mm_df = pd.DataFrame({'id': [], 'mad': [], 'weighted_mean': [],
#         'chi2red': [], 'weighted_stdev': []})

# for i in tqdm(range(len(ea)), desc='progress...', position=0, leave=True):
#     #print(ea[i])
#     mm_df = get_data(mm_df, ea[i])

# # save results!
# print('saving results!')
# mm_name='test.csv'
# mm_df.to_csv(os.path.join(VAR_OUT, mm_name))
