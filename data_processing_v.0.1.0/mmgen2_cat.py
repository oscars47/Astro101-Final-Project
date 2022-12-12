# file to generate the monster matrix (mm) of the contact binaries
# by @oscars47 and @ghirsch123

import os
from tqdm import tqdm
import pandas as pd
import numpy as np
from prettytable import PrettyTable
# import files we've created
from lcgen import get_lc
from vargen import Variable
from vargen2 import Variable2


# NEED TO DO: 
# 1. extract numerical ids from the Catalina phot, get ra and dec -- weird bc the csv is all one columns
# 2. generate asii table, then get color csv
# 3. run objects through variable generator









# set directories, define helper functions for conversions

DATA_DIR = '/home/oscar47/Desktop/astro101/data/contact_binaries'
VAR_OUT = os.path.join(DATA_DIR, 'var_output')

# confirm we have each of these directories
if not(os.path.isdir(VAR_OUT)):
    os.makedirs(VAR_OUT)

# read in datasets---------------
vars = pd.read_csv(os.path.join(DATA_DIR, 'CatalinaVars.csv'))
lc_df = pd.read_csv(os.path.join(DATA_DIR, 'AllVar.phot.csv'))

#print(vars.head(10))

# need to extract numerial ides from lc_df to build df
def build_cat_main():
    ids = []
    ras =[]
    decs = []
    for i in range(len(vars)):
        row = vars.iloc[i][0]
        s_row = row.split('  ')
        id = int(s_row[1])
        ra = float(s_row[2]) # need to convert ra and dec into decimal from sexigesimal!!
        dec = float(s_row[3])
        r_ra = np.round(ra, 5)
        r_dec = np.round(dec, 5)
        ids.append(id)
        ras.append(r_ra)
        decs.append(r_dec)

    # create new dataframe
    cat_main = pd.DataFrame()
    cat_main['id'] = ids
    cat_main['ra'] = ras
    cat_main['dec'] = decs
    # now save it
    cat_main.to_csv(os.path.join(DATA_DIR, 'cat_main.csv'))

build_cat_main()

# load in rounded dfs
# asassn = pd.read_csv(os.path.join(DATA_DIR, 'asassn_rounded.csv'))
# table = pd.read_csv(os.path.join(DATA_DIR, 'table_rounded.csv'))

# helper files to amend datasets----------------------------
# export ra and dec to make ascii table given pd dataframe
# use https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-dd to extract color info
# when you use output from function below, need to delete top and bottom +----+ decorations, then cut the |ra dec| |float float| lines, cntrl-f '|'| replace ' ', then paste back and submit to online portal
def get_ascii(df, save_path):
    #df = df.head(10)

    # get list of ra, dec and add to x
    ra_ls = df['RAJ2000'].to_list()
    dec_ls = df['DEJ2000'].to_list()
   
    x = PrettyTable()

    column_names = ["ra", "dec"]
    ra_ls.insert(0, 'float')
    dec_ls.insert(0, 'float')
    
    x.add_column(column_names[0], ra_ls)
    x.add_column(column_names[1], dec_ls)  

    print(x)

    data = x.get_string()

    with open(os.path.join(save_path, 'test.txt'), 'w') as f:
        f.write(data)

get_ascii(vars, DATA_DIR)
        
# add rounded ra, dec column to asassn
def add_rounding_cat(df):
    ra = df['Ra'].to_list()
    dec = df['Dec'].to_list()
    r_ra = np.round(ra, 5)
    r_dec = np.round(dec, 5)
    df['rounded ra'] = r_ra
    df['rounded dec'] = r_dec

    df.to_csv(os.path.join(DATA_DIR, 'cat_rounded.csv'))

add_rounding_cat(vars)

# add rounding to table output
def add_rounding_table(df):
    ra = df['ra_01'].to_list()
    dec = df['dec_01'].to_list()
    r_ra = np.round(ra, 5)
    r_dec = np.round(dec, 5)
    df['rounded ra'] = r_ra
    df['rounded dec'] = r_dec

    df.to_csv(os.path.join(DATA_DIR, 'table_rounded.csv'))

table_df = pd.read_csv(os.path.join(DATA_DIR, 'table_irsa_catalog_search_results.csv'))
#add_rounding_table(table_df)

# initiate var dfs for Variable2 object
def init_var2_dfs():
    mm_df = pd.DataFrame({
        'name': [], 'target': [], 'period': [], 'power': [],
        'T_t': [], 'T_p': [], 'T_2p': [], 
        'delta_t': [], 'delta_p': [],
        'j-k': [], 'h-k': [], 'skew': [],
        'kurtosis': [], 'stdev': [], 'median': [],
        'iqr': [], 'mad': [], 'von neumann': [],
        'a_hl': [],
        'weighted mean': [],
        'chi2red': [], 'weighted stdev': [],
        'roms': [], 'norm excess var': [], 
        'peak peak var': [], 'lag1 auto': [],
        'I': [],'Ifi': [], 'J': [], 'K': [], 'L': [],
        'J time': [], 'I clipped': [],
        'J clipped': [],
        'Ex': [], 'SB': [],'clipped stdev': []
        })
    return mm_df

# function to take in id and cleanup name to get lc--------------------
def get_var_data_name(df, name, input):
    temp_file = get_file(name)
    target = vars.loc[vars['ID']==name]['ML_classification'].to_list()[0]
    # create new instance of Variable object
    #temp_var = Variable(temp_file, name, isper, target, input)
    temp_var = Variable2(vars, table_df, temp_file, name, target, input)
    temp_df = pd.DataFrame(temp_var.return_dict())
    #df_new = pd.concat([df, temp_df], ignore_index=True)
    df_new = df.append(temp_df.return_dict(), ignore_index=True)
    return df_new

# takes in file name, not id name
def get_var_data_file(df, file, input):
    temp_name = get_name(file)
    target = vars.loc[vars['ID']==temp_name]['ML_classification'].to_list()[0]
    # create new instance of Variable object
    #temp_var = Variable(file, temp_name, isper, target, input)
    temp_var = Variable2(asassn, table, file, temp_name, target, input)
    temp_df = pd.DataFrame(temp_var.return_dict())
    df_new = pd.concat([df, temp_df], ignore_index=True)
    #df_new = df.append(temp_var.return_dict(), ignore_index=True)
    return df_new


# take in a column and returns normalized version
def normalize_col(col):
    # compute min
    col_min = min(col)
    col_max = max(col)

    if col_max - col_min > 0:
        col_n = []
        for x in col:
            x_n = (x - col_min) / (col_max - col_min)
            col_n.append(x_n)
        return col_n

    elif (col_max - col_min == 0) and (col_min > 0):
        col_n = []
        for x in col:
            x_n = (x - col_min) / (col_max)
            col_n.append(x_n)
        return col_n
        
    # everything is 0
    else:
        return col

    
# normalize the data for our NN!
def normalize_master_file(data_path):
    # read the csv: un-normalized df
    un_df = pd.read_csv(data_path)
    #un_df = un_df.head(10)
    var_indices_ls = list(un_df.columns)[4:]
    # go through each column and separately normalize
    for col_name, values in un_df[var_indices_ls].iteritems():
        #print(values)
        temp_col = normalize_col(values)
        un_df[col_name] = temp_col
    # drop one of the duplicate indexing cols
    un_df = un_df.iloc[:, 1:]
    return un_df

def normalize_master_df(un_df):
    var_indices_ls = list(un_df.columns)[2:]
    # go through each column and separately normalize
    for col_name, values in un_df[var_indices_ls].iteritems():
        #print(values)
        temp_col = normalize_col(values)
        un_df[col_name] = temp_col
    # drop one of the duplicate indexing cols
    un_df = un_df.iloc[:, 1:]
    return un_df

def run_all():
    mm_df = init_var2_dfs()
    for i in tqdm(range(len(lc_files)), desc='progress...', position=0, leave=True):
        file = lc_files[i]
        mm_df = get_var_data_file(mm_df, file, LC_DIR)

    # save unnormalized
    mm_df.to_csv(os.path.join(VAR_OUT, 'v0.1.0/mm_2_un.csv'))

    # normalize
    mm_df = normalize_master_df(mm_df)
    # save
    mm_df.to_csv(os.path.join(VAR_OUT, 'v0.1.0/mm_2.csv'))
        
    return mm_df

#mm_df = run_all()
# read in and normalize
#un_df = pd.read_csv(os.path.join(VAR_OUT, 'v0.1.0/mm_2_un.csv'))
#n_df = normalize_master_df(un_df)
#n_df.to_csv(os.path.join(VAR_OUT, 'v0.1.0/mm_2_n.csv'))