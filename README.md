# Astro101-Final-Project
A repo for @oscars47's and @ghirsch123 Astro101 final project (Phil Choi, Pomona College) using machine learning on variable stars.

## Project Goals:
1. We want to test the viability of 23 variability functions we explored over the summer via creating a neural network to classify the types of variable stars in the ASAS-SN data.
2. Once we have established a working trained model, then we can use this as a basis for performing unsupervised clustering in order to determine how our quantification tools developed with the supervised model translate to this unsupervised situation. 
3. Using what we’ve learned with unsupervised clustering in step 2, we will investigate some more well-studied class of variable object with distinct sub-classes (e.g., Cepheids).
4. Using our experience with step 3, we can apply these techniques to the Marsh et al contact binary data to investigate contact binary features.

## Abstract:
We present a project using the ASAS-SN catalog (\cite{christy_asas-sn_2022}) \footnote{\url{https://asas-sn.osu.edu/variables/}} as the data of focus for supervised and unsupervised neural networks we implement to classify variable stars. We outline a plan to use \cite{marsh_characterization_2017} to identify unique subclusters within the contact binary systems. We give an example neural network using the famous iris dataset (\cite{kaggle_iris_2017}) as an illustration of our technique; we also describe the theoretical workings of three unsupervised algorithms---K-Means, OPTICS, and DBSCAN. We define a list of 36 variability indices---included with formulae and comments in the Appendix---to quantify lightcurves, which serves as the actual input data for the networks. Our supervised model has $> 85\%$ accuracy when run on unseen ASAS-SN data, illustrating that our variability indices do a reasonably good job of discriminating variability type. Our unsupervised attempts, however, generate no usable clusters, but reveal some problems with our data preparation and inform future directions for the project. All the code we have written, along with our data products, is freely available and documented on GitHub. \footnote{\url{https://github.com/oscars47/Astro101-Final-Project}}

## Data products:
Link to datasets generated via the data_processing pipeline: https://drive.google.com/drive/folders/1PgVBjVWzdmSGbx42nixHeabedoXOK9Cl?usp=sharing
