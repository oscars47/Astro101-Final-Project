# file to generate lightcurves
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

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
        for i, t in enumerate(time):
            time[i]=float(t)
        mag = lc_df['mag'].to_list()
        for i, m in enumerate(mag):
            if isinstance(m, str):
                if ('>' in m) or ('<' in m):
                    m=m[1:]
                    mag[i]=float(m)
                else:
                    mag[i]=float(m)
        mag_err = lc_df['mag_err'].to_list()
        for i, m in enumerate(mag_err):
            if isinstance(m, str):
                mag_err[i]=float(m)


        print(len(time))
        print(len(mag))
        print(len(mag_err))

        # remove bad mag errs
        for i, elem in enumerate(mag_err):
            print(type(elem))
            if elem > 99:
                print('error: mag_err=', elem)
                mag_err[i]=0.0
        print(mag)
        # define figure
        plt.figure(figsize=(10, 5))
        plt.scatter(time, mag)
        plt.errorbar(time, mag, yerr=mag_err, fmt='o', color='purple')
        plt.xlabel('Time (HJD)', fontsize=10)
        plt.ylabel('Mag', fontsize=10)
        plt.title('Unfolded LC for Object ' + name +': ' + target, fontsize=12)
        plt.savefig(output+'/'+target+'lc_%s.jpeg'%name)
        plt.close()

        # if not(max(mag_err) > 5):
        #     # define figure
        #     plt.figure(figsize=(10, 5))
        #     plt.scatter(time, mag)
        #     plt.errorbar(time, mag, yerr=mag_err, fmt='o', color='purple')
        #     plt.xlabel('Time (HJD)', fontsize=14)
        #     plt.ylabel('Mag', fontsize=14)
        #     plt.title('Unfolded LC for Object ' + name +': ' + target, fontsize=16)
        #     plt.savefig(output+'/'+target+'lc_%s.jpeg'%name)
        #     plt.close()
        # else:
        #     print('err: max err value %f exceeds 5 mag limit'%max(mag_err))
        # except:
        #     print('lightcurve %s could not be created.' %file)
    else:
        print('error. must load .dat file. your file is:', file)

def get_lc_fold(file, name, target, input, period, output, per_type):
    if file.endswith('.dat'):
        #try:
        # create dataframe
        c_path = os.path.join(input, file)
        lc_df = pd.read_csv(c_path, sep='\t')
        
        # the columns we want are time, mag and mag err
        time = np.array(lc_df['HJD'].to_list()) # convert to numpy array to fold
        time = time % period
        time = list(time)
        mag = lc_df['mag'].to_list()
        mag_err = lc_df['mag_err'].to_list()

        for i, m in enumerate(mag):
            if isinstance(m, str):
                if ('>' in m) or ('<' in m):
                    m=m[1:]
                    mag[i]=float(m)
                else:
                    mag[i]=float(m)
     
        for i, m in enumerate(mag_err):
            if isinstance(m, str):
                mag_err[i]=float(m)


        print(len(time))
        print(len(mag))
        print(len(mag_err))

        # remove bad mag errs
        for i, elem in enumerate(mag_err):
            print(type(elem))
            if elem > 99:
                print('error: mag_err=', elem)
                mag_err[i]=0.0
        print(mag_err)
        # define figure
        plt.figure(figsize=(10, 5))
        plt.scatter(time, mag)
        plt.errorbar(time, mag, yerr=mag_err, fmt='o', color='purple')
        plt.xlabel('Time (HJD)', fontsize=10)
        plt.ylabel('Mag', fontsize=10)
        plt.title('Folded LC (' + per_type + '), P = '+ f'{period:.6f}' + ' d for Object ' + name + ': ' + target, fontsize=12)
        plt.savefig(output+'/'+target+'lc_folded_%s_%s.jpeg'%(name, per_type))
        plt.close()
        
        # if not(max(mag_err) > 5):
        #     # define figure
        #     plt.figure(figsize=(10, 5))
        #     plt.scatter(time, mag)
        #     plt.errorbar(time, mag, yerr=mag_err, fmt='o', color='purple')
        #     plt.xlabel('Time (HJD)', fontsize=14)
        #     plt.ylabel('Mag', fontsize=14)
        #     plt.title('Folded LC (' + per_type + '), P = '+ str(period) + ' d for Object ' + name + ': ' + target, fontsize=16)
        #     plt.savefig(output+'/'+target+'lc_folded_%s_%s.jpeg'%(name, per_type))
        #     plt.close()
        # else:
        #     print('err: max err value %f exceeds 5 mag limit'%max(mag_err))
        # except:
        #     print('lightcurve %s could not be created.' %file)
    else:
        print('error. must load .dat file. your file is:', file)

    
