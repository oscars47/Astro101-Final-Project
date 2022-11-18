import os
import numpy as np
import pandas as pd
from keras.models import load_model

from nnprep import *

# load model
MODEL_PATH = '/home/oscar47/Desktop/astro101/models'
model = load_model(os.path.join(MODEL_PATH, 'lilac19.h5'))

# load input_x and output targets
DATA_DIR = '/home/oscar47/Desktop/astro101/data/g_band/var_output'


input_x = np.load(os.path.join(DATA_DIR, 'mm_n_extra.npy'))
output_targets = np.load(os.path.join(DATA_DIR, 'targets_extra.npy'))


#load asasn-sn variables in last 50%
asassn = pd.read_csv(os.path.join(DATA_DIR, 'folded_mm_per.csv'))
min_index = int(0.5*len(asassn))
asassn = asassn.iloc[min_index:, :]

# takes in input probability vector
def convert_to_class(vec):
    # find index of largest arg
    index = np.argmax(vec)
    confidence = np.max(vec)
    class_type = int_to_class[index]
    return class_type, confidence

# get class names
object_names = asassn['id'].to_list()
object_target_real = asassn['target'].to_list()

print(unique_targets)
test = output_targets[2]
print(test)
print(convert_to_class(test))
print(object_target_real[2])
print(make_1_hots([object_target_real[2]]))

# takes in input data which is array of arrays
def predict_vars(model, names, input_x, output_targets, targets2, file_name):
    results = model.predict(input_x) # predict!!
    # initialize lists to hold results
    output_classes = []
    output_confidences= []
    for result in results:
        class_type, confidence = convert_to_class(result)
        output_classes.append(class_type)
        output_confidences.append(confidence)

    #convert targets back to classes
    output_target_names = []
    for target in output_targets:
        class_type, _ = convert_to_class(target)
        output_target_names.append(class_type)

    # build and save dataset
    asassn_pred = pd.DataFrame()
    asassn_pred['ID'] = names
    asassn_pred['prediction'] = output_classes
    asassn_pred['confidence'] = output_confidences
    asassn_pred['actual'] = output_target_names
    asassn_pred['actual2'] = targets2
    
    asassn_pred.to_csv(os.path.join(DATA_DIR, file_name))
    #return asassn_pred
file_name = 'lilac19_results.csv'
lilac19 = predict_vars(model, object_names, input_x, output_targets, object_target_real, file_name)