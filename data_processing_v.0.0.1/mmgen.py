# file to generate the monster matrix (mm) of var indices data for each lc object
# by @oscars47 and @ghirsch123

import os
from tqdm import tqdm
import pandas as pd
# import files we've created
from lcgen import get_lc
from vargen import Variable

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
def get_data(df, name):
    temp_list = []
    temp_file = ''
    temp_list = name.split(' ')
    temp_file += temp_list[0] +'_' + temp_list[1] +'.dat'

    #get_lc(temp_file, name, LC_DIR, LC_OUT)
    # create new instance of Variable object
    temp_var = Variable(temp_file, name, LC_DIR)
    df = df.append(temp_var.return_dict(), ignore_index=True)
    return df

# create new df --- the monster matrix --- to hold results of Variable obj
mm_df = pd.DataFrame({'id': [], 'mad': [], 'weighted_mean': [],
        'chi2red': [], 'weighted_stdev': []})

for i in tqdm(range(len(ea)), desc='progress...', position=0, leave=True):
    #print(ea[i])
    mm_df = get_data(mm_df, ea[i])

# save results!
print('saving results!')
mm_name='test.csv'
mm_df.to_csv(os.path.join(VAR_OUT, mm_name))
