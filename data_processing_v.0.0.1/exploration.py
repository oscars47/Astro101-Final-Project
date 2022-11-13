# file to create sample lighcurves for various classes of objects and compute their variability indices
import os
from tqdm import tqdm
import pandas as pd
# import files we've created
from lcgen import get_lc

DATA_DIR = '/home/oscar47/Desktop/astro101/data/g_band'
LC_DIR = os.path.join(DATA_DIR, 'g_band_lcs')
LC_OUT = os.path.join(DATA_DIR, 'lc_output')
VAR_OUT = os.path.join(DATA_DIR, 'var_output')

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

# get test object--------------
# lc_47 = lc_files[47]
# lc_47_name = lc_names[47]
# LC_DIR = os.path.join(DATA_DIR, 'g_band_lcs')
# get_lc(lc_47, lc_47_name, LC_DIR, LC_OUT)

# get unique classes of variable objects
vars = pd.read_csv(os.path.join(DATA_DIR, 'asassn_variables_x.csv'))
var_unique = list(vars['ML_classification'].unique())

# for testing, let's get HADS, RVA
hads = vars.loc[vars['ML_classification']=='HADS']['ID'].to_list()
ea = vars.loc[vars['ML_classification']=='EA']['ID'].to_list()

# just take first 10
ea = ea[:10]
print(ea)

# function to take in id and cleanup name to get lc--------------------
def get_data(name):
    temp_list = []
    temp_file = ''
    temp_list = name.split(' ')
    temp_file += temp_list[0] +'_' + temp_list[1] +'.dat'

    get_lc(temp_file, name, LC_DIR, LC_OUT)
    # call get_var_data here

for i in tqdm(range(len(ea)), desc='progress...', position=0, leave=True):
    #print(ea[i])
    get_data(ea[i])
# print(ea[5])
# get_data(ea[5])
