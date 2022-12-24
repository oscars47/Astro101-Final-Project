# Astro101-Final-Project
A repositoey for @oscars47's and @ghirsch123 Astro101 final project (Phil Choi, Pomona College) using machine learning on variable stars.

## Abstract:
We present a project using the ASAS-SN catalog (https://asas-sn.osu.edu/variables/) as the data of focus for supervised and unsupervised neural networks we implement to classify variable stars. We outline a plan to use the Marsh et al 2017 data to identify unique subclusters within the contact binary systems. We give an example neural network using the famous iris dataset (https://www.kaggle.com/datasets/vikrishnan/iris-dataset) as an illustration of our technique; we also describe the theoretical workings of three unsupervised algorithms---K-Means, OPTICS, and DBSCAN. We define a list of 36 variability indices---included with formulae and comments in the Appendix---to quantify lightcurves, which serves as the actual input data for the networks. Our supervised model has >85% accuracy when run on unseen ASAS-SN data, illustrating that our variability indices do a reasonably good job of discriminating variability type. Our unsupervised attempts, however, generate no usable clusters, but reveal some problems with our data preparation and inform future directions for the project. All the code we have written, along with our data products, is freely available and documented on this repository.


## Data products:
Link to datasets generated via the data_processing pipeline: https://drive.google.com/drive/folders/1PgVBjVWzdmSGbx42nixHeabedoXOK9Cl?usp=sharing

## Samples of results
![final_flow_down](https://user-images.githubusercontent.com/106777951/208241323-d30c3cb9-f709-4421-ba13-9eae762af961.png)
Flow chart for the code in this project.

![Flowers NN](https://user-images.githubusercontent.com/106777951/208241586-ef088cd4-8cdf-4d36-9a20-8186f9e84a86.png)
Example neural network implemnted from scratch on iris data as an illustration of how neural nets work.

![confusion_0 1 1_mini](https://user-images.githubusercontent.com/106777951/208241192-3c327e34-982d-48a4-afd4-68f249bf2880.png)
Confusion matrix for version 0.1.1 mini.

![mini-1](https://user-images.githubusercontent.com/106777951/208241458-eb0d4c06-a0fe-41c0-925d-2274924ddab1.png)
3D plot of v0.1.1 mini confusion matrix.

![per200_5000](https://user-images.githubusercontent.com/106777951/208241649-af5dc242-2969-4850-96e2-0bd923dfae13.png)
t-SNE plot of 25% of data, using perplexity=200 and N_iterations=5000.

![optics](https://user-images.githubusercontent.com/106777951/208241560-4322910f-d007-4892-99bc-da021d0cc223.png)
Plot showing the t-SNE representation (perplexity=200, N_iterations=5000) clustered using the OPTICS algorithm.

![linear_random_per](https://user-images.githubusercontent.com/106777951/208241498-b1c98b36-0d33-454b-ba30-29f69fde2133.png)
Comparison of sample sample of objects' ASAS-SN and Monster Matrix periods.



