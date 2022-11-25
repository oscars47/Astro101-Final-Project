# file holding Variable2 object functions to reflect paper
# @oscars47

import os
import numpy as np
import pandas as pd
from astropy.timeseries import LombScargle
import matplotlib.pyplot as plt
from lcgen import get_lc

DATA_DIR = '/home/oscar47/Desktop/astro101/data/g_band'
LC_DIR = os.path.join(DATA_DIR, 'g_band_lcs')

asassn = pd.read_csv(os.path.join(DATA_DIR, 'asassn_rounded.csv'))
table = pd.read_csv(os.path.join(DATA_DIR, 'table_rounded.csv'))

names = asassn['ID'].to_list()

# make list of all LC_DIR files
lc_files = os.listdir(LC_DIR)

# function to compute color
def get_color(table, asassn, name):
    name_df = asassn.loc[asassn['ID']==name]
    # get ra and dec; round to 5 decimal places
    as_ra = name_df['rounded ra'].to_list()[0]
    as_dec = name_df['rounded dec'].to_list()[0]
    print(as_ra, as_dec)
    
    try:
        # find in data_df
        table_row = table.loc[(table['rounded ra']==as_ra) & (table['rounded dec']==as_dec)]
        # get values
        j = table_row['j_m'].to_list()[0]
        h = table_row['h_m'].to_list()[0]
        k = table_row['k_m'].to_list()[0]

        return j-k, h-k

    except:
        print('ID %s could not be found in the table dataset' %name)
        return 0, 0

    
# function to compute Lomb-Scargle period and FAP
def get_LS_period(input, file):
    print(file)
    # create dataframe
    c_path = os.path.join(input, file)
    lc_df = pd.read_csv(c_path, sep='\t')
    # initialize time, mag, and mag_err lists
    time_ls = np.array(lc_df['HJD'].to_list()).astype(float)
    # unclean mag_ls
    mag_uc = lc_df['mag'].to_list()
    mag_c = []
    for mag in mag_uc:
        if not ('>' in str(mag)) or ('<' in str(mag)):
            mag_c.append(mag)
        else:
            mag_temp = str(mag)[1:]
            mag_c.append(float(mag_temp))
    #self.mag_ls = np.array(lc_df['mag'].to_list()).astype(float)
    mag_ls = np.array(mag_c).astype(float)
    mag_err_ls = np.array(lc_df['mag_err'].to_list()).astype(float)
    
    ls = LombScargle(time_ls, mag_ls, mag_err_ls, normalization='standard')
    freq, power = ls.autopower(method='fastchi2')
    fap = ls.false_alarm_probability(power.max())

    best_frequency = freq[np.argmax(power)]
    period = 1/ best_frequency

    # let's plot a folded lc
    # time_f = []
    # for time in time_ls:
    #     time_f.append(time % period)
    
    # #print(mag_ls)
    # plt.scatter(time_f, mag_ls)
    # plt.show()
    

    return period, power.max(), fap

# compute the LKLS stat for a given sorted mag_ls
def get_T(mag_ls):
    mean = np.mean(mag_ls)
    num_ls = []
    for i in range(len(mag_ls)-1):
        num_ls.append((mag_ls[i+1] - mag_ls[i])**2)
    num = np.sum(num_ls)
    #print('num', num)

    denom_ls = []
    for mag in mag_ls:
        denom_ls.append((mag - mean)**2)
    denom = np.sum(denom_ls)
    #print('denom', denom)

    N = len(mag_ls)
    return (num / denom) * ((N - 1) / (2*N))

# helper function to sort mag based on folded lc
def sort_fold(time_ls, mag_ls, period):
    # get folded times
    time_f = []
    for time in time_ls:
        time_f.append(time % period)
    
    # now combine into list of tuples
    time_mag = list(zip(time_f, mag_ls))
    #print('unsorted', time_mag)
    # now sort based on modded time, which is 0th index
    time_mag.sort(key=lambda x:x[0])
    #print('sorted', time_mag)
    unzipped= list(zip(*time_mag))
    s_time, s_mag = unzipped[0], unzipped[1]
    return s_mag # return the sorted mag

# lafler kinmann string length statistic
def get_LKLS(period, input, file):
    print(file)
    # create dataframe
    c_path = os.path.join(input, file)
    lc_df = pd.read_csv(c_path, sep='\t')
    # initialize time, mag, and mag_err lists
    time_ls = np.array(lc_df['HJD'].to_list()).astype(float)
    # unclean mag_ls
    mag_uc = lc_df['mag'].to_list()
    mag_c = []
    for mag in mag_uc:
        if not ('>' in str(mag)) or ('<' in str(mag)):
            mag_c.append(mag)
        else:
            mag_temp = str(mag)[1:]
            mag_c.append(float(mag_temp))
    #self.mag_ls = np.array(lc_df['mag'].to_list()).astype(float)
    mag_ls = np.array(mag_c).astype(float)
    mag_err_ls = np.array(lc_df['mag_err'].to_list()).astype(float)


    # compute T for time
    T_t = get_T(mag_ls)

    # sort mag_ls based on period and twice period
    s1_mag = sort_fold(time_ls, mag_ls, period)
    s2_mag = sort_fold(time_ls, mag_ls, 2*period)
    # T for period
    T_p = get_T(s1_mag)
    T_2p = get_T(s2_mag)

    # compute delta_t and delta_p
    delta_t = (T_p - T_t) / T_t
    delta_p = (T_2p - T_p) / T_p

    return T_t, T_p, T_2p, delta_t, delta_p

period, power, fap = get_LS_period(LC_DIR, lc_files[4])
print(get_LKLS(period, LC_DIR, lc_files[4]))
print(asassn.loc[asassn['ID']=='ASASSN-V J164336.01-665428.4']['LKSL_statistic'])
#print(get_color(table, asassn, names[0]))