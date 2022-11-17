# file to generate confusion matrix to investigate what var indices to use

import pandas as pd
import os
import numpy as np
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt

DATA_DIR = '/home/oscar47/Desktop/astro101/data/g_band/var_output/'

# read in csv
global mm_n, unique_targets, targets
mm_n = pd.read_csv(os.path.join(DATA_DIR,'folded_mm_per_norm.csv'))
targets = mm_n['target'].to_list()
unique_targets = list(set(targets))
mm_n = mm_n.iloc[:, 4:]

def get_heatmap():
    # print(mm_n.head(5))
    matrix = mm_n.corr().round(3)
    sns.heatmap(matrix, annot=True)
    plt.savefig(os.path.join(DATA_DIR, 'heatmap.jpeg'))
    plt.show()

# these hold the conversion from the list of var classes to indices in the list and vice versa
def get_target_dicts():
    global class_to_int, int_to_class
    class_to_int = dict((target, i) for i, target in enumerate(unique_targets))
    int_to_class = dict((i, target) for i, target in enumerate(unique_targets))
    return class_to_int, int_to_class

def prep_data():
    # first split 50-50; return a dataset to be used to validate
    init_split_index = int(0.5*len(mm_n))
    # train-validate portion
    mm_n_tv = mm_n.iloc[:init_split_index, :]
    mm_n_extra = mm_n.iloc[init_split_index:, :]

    # convert the targets into 1 hot encoded vectors
    class_to_int, _ = get_target_dicts()
    # make our 1 hot encoded vectors
    target_1_hots = []
    for target in targets:
        # get the index
        index = class_to_int[target]
        # initialize 0 vector
        vec = np.zeros(len(unique_targets))
        # place 1 at index location
        vec[index] = 1
        target_1_hots.append(vec)

    targets_tv = target_1_hots[:init_split_index]
    targets_extra = target_1_hots[init_split_index:]


    # split within tv dataset
    train_split_index = int(0.8*len(mm_n_tv))
    train_x_ds = mm_n_tv.iloc[:train_split_index, :]
    val_x_ds = mm_n_tv.iloc[train_split_index:, :]
    train_y_ds = targets_tv[:train_split_index]
    val_y_ds = targets_tv[train_split_index:]

    # convert to numpy arrays
    train_x_ds = train_x_ds.to_numpy()
    val_x_ds = val_x_ds.to_numpy()
    train_y_ds = np.array(train_y_ds)
    val_y_ds = np.array(val_y_ds)

    
    mm_n_extra = mm_n_extra.to_numpy()
    targets_extra = np.array(targets_extra)

    # save!!
    print('saving datasets!')
    np.save(os.path.join(DATA_DIR, 'train_x_ds.npy'), train_x_ds)
    np.save(os.path.join(DATA_DIR, 'val_x_ds.npy'), val_x_ds)
    np.save(os.path.join(DATA_DIR, 'train_y_ds.npy'), train_y_ds)
    np.save(os.path.join(DATA_DIR, 'val_y_ds.npy'), val_y_ds)

    np.save(os.path.join(DATA_DIR, 'mm_n_extra.npy'), mm_n_extra)
    np.save(os.path.join(DATA_DIR, 'targets_extra.npy'), targets_extra)

prep_data()
train_x_ds = np.load(os.path.join(DATA_DIR, 'train_x_ds.npy'))
val_y_ds = np.load(os.path.join(DATA_DIR, 'val_y_ds.npy'))

#print(train_x_ds)
# print('-------')
# for ls in val_y_ds:
#     print(ls)


