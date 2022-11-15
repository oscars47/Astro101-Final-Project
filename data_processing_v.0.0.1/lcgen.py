# file to generate lightcurves
import matplotlib.pyplot as plt
import os
import pandas as pd

# reads in .dat file along with output directory
# target is what the class label in the ASAS-SN dataset is
def get_lc(file, name, target, input, output):
    if file.endswith('.dat'):
        #try:
        # create dataframe
        c_path = os.path.join(input, file)
        lc_df = pd.read_csv(c_path, sep='\t')
        
        # the columns we want are time, mag and mag err
        time = lc_df['HJD'].to_list()
        mag = lc_df['mag'].to_list()
        mag_err = lc_df['mag_err'].to_list()
        
        if not(max(mag_err) > 5):
            # define figure
            plt.figure(figsize=(10, 5))
            plt.scatter(time, mag)
            plt.errorbar(time, mag, yerr=mag_err, fmt='o', color='purple')
            plt.xlabel('time (HJD)', fontsize=14)
            plt.ylabel('mag', fontsize=14)
            plt.title('lightcurve for object ' + name, fontsize=16)
            plt.savefig(output+'/'+target+'lc_%s.jpeg'%name)
        else:
            print('err: max err value %f exceeds 5 mag limit'%max(mag_err))
        # except:
        #     print('lightcurve %s could not be created.' %file)
    else:
        print('error. must load .dat file. your file is:', file)

    
