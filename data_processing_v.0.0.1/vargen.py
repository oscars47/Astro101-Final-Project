# created by @oscars47 and @ghirsch123 summer 2022, updated fall 2022
# creates a class called Variable that computes each of the 23 indices for each lightcurve object passed through
# if max(mag_err) exceeds 5, then return null for each value and include "bad" flag; remove all obejcts that have bad flag in final df

import numpy as np
import pandas as pd
import os

# assumes input is single .dat file for the variable of interest
class Variable:
    # initializing-----------------------------
    def __init__(self, file, name, input):
        
        # create dataframe
        c_path = os.path.join(input, file)
        lc_df = pd.read_csv(c_path, sep='\t')
        # initialize time, mag, and mag_err lists
        self.time_ls = np.array(lc_df['HJD'].to_list()).astype(float)
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
        self.mag_ls = np.array(mag_c).astype(float)
        self.mag_err_ls = np.array(lc_df['mag_err'].to_list()).astype(float)

        # set name to be its id
        self.name = name

        # initialize each of the var indices
        self.mad = self.get_mad()
        self.weighted_mean = self.get_weighted_mean()
        self.chi2red = self.get_chi2red()
        self.weighted_stdev = self.get_weighted_stdev()
    
    # creating var function---------------------
    def get_mad(self):
        #compute median of mag_list
        median_mag = np.median(self.mag_ls)
        
        #now compute absolute deviations from the median
        absolute_deviations_list = []
        for mag in self.mag_ls:
            absolute_deviations_list.append(abs(mag - median_mag)) 
            
        #compute median of the absolute deviations; this is MAD!
        mad = np.median(absolute_deviations_list)
        
        return mad

    def get_weighted_mean(self):
        #create empty lists to sum at end
        weighted_mean_num_list = []
        weighted_mean_denom_list = []
        for i, magerr in enumerate(self.mag_err_ls):
            weighted_mean_num_list.append(
                self.mag_ls[i] / (magerr**2)
            )
            
            weighted_mean_denom_list.append(
                1 / (magerr**2)
            ) 
        weighted_mean = sum(weighted_mean_num_list) / sum(weighted_mean_denom_list)
        return weighted_mean
    
    def get_chi2red(self):
         #chi2-------
        chi2_list = []
        for i, mag in enumerate(self.mag_ls):
            chi2_list.append(
                ((mag - self.weighted_mean)**2) / (self.mag_err_ls[i]**2)
            )
            
        chi2 = sum(chi2_list)
        
        #chi2 reduced-----
        chi2_red = chi2 / (len(self.mag_ls) - 1)
        return chi2_red
    
    def get_weighted_stdev(self):
        #calculate first term multiplying the sum of the weights*(mag - magerr)^2
        weights_list = []
        square_weights_list = []
        for magerr in self.mag_err_ls:
            weight = 1 / (magerr**2)
            weights_list.append(weight)
            square_weights_list.append(weight**2)
            
        left_term = sum(weights_list) / ((sum(weights_list)**2) - sum(square_weights_list))
        
        right_term_list = []
        for i, mag in enumerate(self.mag_ls):
            right_term_list.append(
                weights_list[i]*((mag - self.weighted_mean)**2)
            )
            
        right_term = sum(right_term_list)
        
        #return square root of left term * right term
        weighted_std_dev = (left_term * right_term)**0.5
        return weighted_std_dev


    # compile all stats into dataframe entry; return dict
    def return_dict(self):
        return {'id': self.name, 'mad': self.mad, 'weighted_mean': self.weighted_mean,
        'chi2red': self.chi2red, 'weighted_stdev': self.weighted_stdev}
