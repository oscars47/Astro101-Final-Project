# file to try unsupervised clustering, implement the OPTICS algorithm
# @oscars47

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import plotly.express as px

# set directories to normalized data
DATA_DIR = '/home/oscar47/Desktop/astro101/data/g_band/var_output/v0.1.1'
OUTPUT_DIR = os.path.join(DATA_DIR, 'unsupervised')

# read in data with actual targets for verification
mm_n = pd.read_csv(os.path.join(DATA_DIR, 'mm_2_n_targ_var.csv'))
targets = mm_n['target'].to_list()
# now renove the final column of targets as well as first 2
mm_d = mm_n.iloc[:, 2:-1]

# import OPTICS package
from sklearn.cluster import OPTICS
# choose minimum number of samples as the number of dimensions in data + 1

def run(min_samples, percent, filename):
    min_samples = 10
    # reduced data set
    r_index = int(percent*len(mm_d))
    mm_r = mm_d.iloc[:r_index, :].copy()
    # get actual classes for validation
    targets_r = targets[:r_index]
    print(len(mm_r))
    optics_clustering = OPTICS(min_samples=min_samples).fit(mm_r)
    labels = optics_clustering.labels_
    print('unique labels', set(labels))

    mm_r['prediction']=labels
    mm_r['targets'] = targets_r
    mm_r.to_csv(os.path.join(OUTPUT_DIR, filename))

# function to do unsupervised clustering but using PCA data
def run_PCA(min_samples, percent, filename):
    name = filename.split('.') # remove csv so we can concatenate pc

    mm_r = pd.read_csv(os.path.join(OUTPUT_DIR, name[0]+'_pc.csv'))

    r_index = int(percent*len(mm_d))
    targets_r = targets[:r_index]

    optics_clustering = OPTICS(min_samples=min_samples).fit(mm_r)
    labels = optics_clustering.labels_
    print('unique labels', set(labels))

    mm_r['prediction']=labels
    mm_r['targets'] = targets_r
    mm_r.to_csv(os.path.join(OUTPUT_DIR, filename))

# function to generate PCA
def get_PCA(filename):
    mm_r = pd.read_csv(os.path.join(OUTPUT_DIR, filename))

    # remove last 2 cols and perform 3 component PCA
    mm_r = mm_r.iloc[:, :-2]

    pca = PCA(n_components=3)
    principal_components = pca.fit_transform(mm_r)
    var = np.sum(pca.explained_variance_ratio_)

    print('variance', var)

    # get new df
    pc_df = pd.DataFrame(data=principal_components, columns=['pc1', 'pc2', 'pc3'])
    name = filename.split('.') # remove csv so we can concatenate pc
    pc_df.to_csv(os.path.join(OUTPUT_DIR, name[0]+'_pc.csv'))

    return var # return the variance

# function for visualizing results
def plot_preds(filename, var, percent):
    mm_r = pd.read_csv(os.path.join(OUTPUT_DIR, filename))
    predictions = mm_r['prediction'].to_list() # get targets and preds
    targs = mm_r['targets'].to_list()

    # read in pca
    name = filename.split('.') # remove csv so we can concatenate pc
    pc_df = pd.read_csv(os.path.join(OUTPUT_DIR, name[0]+'_pc.csv'))
    pc_df['predictions']=predictions
    pc_df['targs']=targs

    fig = px.scatter_3d(pc_df, x='pc1', y='pc2', z='pc3',
              color='predictions')
    fig.update_layout(title="PCA on %f Percent of Data, Predictions (var=%f)"%(np.round(percent*100, 2), np.round(var, 4)), autosize=False,
                    width=1000, height=1000)
    fig.show()

    fig = px.scatter_3d(pc_df, x='pc1', y='pc2', z='pc3',
              color='targs')
    fig.update_layout(title="PCA on %f Percent of Data, Targets (var=%f)"%(np.round(percent*100, 2), np.round(var, 4)), autosize=False,
                    width=1000, height=1000)
    fig.show()

filename = 'mm_r_optics_.1_10.csv'
filename_pca = 'mm_r_optics_.1_10_pca.csv'
percent=0.1
min_samples=10
#run(min_samples, percent, filename)
var = get_PCA(filename)
#run_PCA(min_samples, percent, filename_pca)
plot_preds(filename, var, percent)
