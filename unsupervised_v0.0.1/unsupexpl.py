# file to try unsupervised clustering, implement the OPTICS algorithm
# @oscars47

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import plotly.express as px
from tqdm import tqdm

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

# run optics on tsne or pca data
def run_optics_tsne(df, min_samples, outname):
    # save targets
    targets = df['targets'].to_list()
    # now remove them from the df
    df = df.iloc[:, :-1]

    # now call OPTICS
    optics_clustering = OPTICS(min_samples=min_samples).fit(df)
    labels = optics_clustering.labels_
    print('unique labels', set(labels))

    # add back in targets with predictions
    df['targets']=targets
    df['predictions']=labels

    # now save as csv
    df.to_csv(os.path.join(OUTPUT_DIR, outname))


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

# takes in df
def get_TSNE(mm_r, percent, perplexity, n_iterations, outname):
    # get subset of mm_r
    r_index = int(percent*len(mm_d))
    mm_r = mm_d.iloc[:r_index, :].copy()

    # get targets for validation
    targets_r = targets[:r_index]

    # perplexity parameter can be changed based on the input datatset
    # dataset with larger number of variables requires larger perplexity
    # set this value between 5 and 50 (sklearn documentation)
    # verbose=1 displays run time messages
    # set n_iter sufficiently high to resolve the well stabilized cluster
    # get embeddings
    tsne_arr = TSNE(n_components=3, perplexity=perplexity, n_iter=n_iterations, verbose=1).fit_transform(mm_r)
    tsne_df = pd.DataFrame({'tsne1': [], 'tsne2': [], 'tsne3': []})

    for ls in tsne_arr:
        tsne_df = tsne_df.append({'tsne1': ls[0], 'tsne2':ls[1], 'tsne3':ls[2]}, ignore_index=True)
    
    tsne_df['targets'] = targets_r
    
    # print to verify
    print(tsne_df.head(10))

    # save
    print('saving!')
    tsne_df.to_csv(os.path.join(OUTPUT_DIR, outname))

# takes in df; removes indices that are SR or L
def get_TSNE_clipped(mm_r, percent, perplexity, n_iterations, outname):
    # get subset of mm_r
    r_index = int(percent*len(mm_d))

    # get targets for validation
    targets_r = targets[:r_index]
    mm_r = mm_d.iloc[:r_index, :].copy()

    mm_r['targets'] = targets_r
    mm_r = mm_r.loc[(mm_r['targets']!='SR') & (mm_r['targets']!='L')]
    # get new list of targets
    targets_new = mm_r['targets'].to_list()

    # now remove target column again
    mm_r = mm_r.iloc[:, :-1]
    print(len(mm_r))


    # perplexity parameter can be changed based on the input datatset
    # dataset with larger number of variables requires larger perplexity
    # set this value between 5 and 50 (sklearn documentation)
    # verbose=1 displays run time messages
    # set n_iter sufficiently high to resolve the well stabilized cluster
    # get embeddings

    tsne_arr = TSNE(n_components=3, perplexity=perplexity, n_iter=n_iterations, verbose=1).fit_transform(mm_r)
    tsne_df = pd.DataFrame({'tsne1': [], 'tsne2': [], 'tsne3': []})

    for ls in tsne_arr:
        tsne_df = tsne_df.append({'tsne1': ls[0], 'tsne2':ls[1], 'tsne3':ls[2]}, ignore_index=True)
    
    tsne_df['targets'] = targets_new
    
    # print to verify
    print(tsne_df.head(10))

    # save
    print('saving!')
    tsne_df.to_csv(os.path.join(OUTPUT_DIR, outname))

# function to plot dimensionally-reduced data with complete filename
def plot_tsne_test(c_filename, percent, perplexity, n_iterations):
    df = pd.read_csv(os.path.join(OUTPUT_DIR, c_filename))
    # get list of columns
    col_list = df.columns

    fig = px.scatter_3d(df, x='tsne1', y='tsne2', z='tsne3', color='targets')
    fig.update_layout(title='TSNE on %f of Data for Perplexity=%f, N_iterations=%f'%((np.round(percent*100, 2), np.round(perplexity, 2), np.round(n_iterations, 2))), autosize=False,
                    width=1000, height=1000)
    fig.show()

# function for visualizing results---------------------------
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

# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

# function to visualize distribution of objects
def visualize_objs(percent):
    # get subset of mm_r
    r_index = int(percent*len(mm_d))
    # get targets for validation
    targets_r = targets[:r_index]
    # find unique objects, then get their respective counts
    targets_r_unique = list(set(targets_r))
    targets_r_unique_counts = []
    for targ in targets_r_unique:
        targets_r_unique_counts.append(targets_r.count(targ)) # append to list
    # now we can plot
    plt.figure(figsize=(10, 7))
    plt.bar(x=targets_r_unique, height=targets_r_unique_counts, color='magenta')
    addlabels(targets_r_unique, targets_r_unique_counts)
    plt.title('Number of objects per class in first 25%', fontsize=18)
    plt.xlabel('Class', fontsize=16)
    plt.ylabel('Number of objects', fontsize=16)
    plt.show()

# percent=0.25
# # visualize_objs(percent)

# filename = 'mm_r_optics_.25_10.csv'
# filename_pca = 'mm_r_optics_.1_10_pca.csv'
# percent=0.1
# min_samples=10
# run(min_samples, percent, filename)
# var = get_PCA(filename)
# run_PCA(min_samples, percent, filename_pca)
# plot_preds(filename, var, percent)

percent=.25
perplexities=[75, 200, 500, 1000]
n_iterations=[1000, 5000]
for n_iter in tqdm(n_iterations):# loop through all possibilities
    for perplex in tqdm(perplexities):
        outname='tsne_'+str(percent)+'_'+str(perplex)+'_'+str(n_iter)+'_clipped.csv'
        get_TSNE_clipped(mm_d, percent, perplex, n_iter, outname)
        plot_tsne_test(outname, percent, perplex, n_iter)



# for trying a range of perplexities with fixed n_iterations
# perplexity_ls = [30, 50, 75, 200, 500, 1000, 2000]
# percent = .25
# n_iterations = 5000
# for perplexity in perplexity_ls:
#     outname='tsne_'+str(percent)+'_'+str(perplexity)+'_'+str(n_iterations)+'.csv'
#     get_TSNE(mm_d, percent, perplexity, n_iterations, outname)
#     plot_tsne_test(outname, percent, perplexity, n_iterations)