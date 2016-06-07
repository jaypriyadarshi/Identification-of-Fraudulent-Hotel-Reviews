# Identification-of-Fraudulent-Hotel-Reviews
Python program to classify hotel reviews into four classes: Truthful, Deceptive, Positive and Negative Reviews 

A naive Bayes classifier to identify hotel reviews as either truthful or deceptive, and either positive or negative. Used word tokens as features for classification.

nblearn.py will learn a naive Bayes model from the training data, and nbclassify.py will use the model to classify new data.
The learning program will be invoked in the following way:

> python nblearn.py /path/to/input

The argument is the directory of the training data; the program will learn a naive Bayes model, and write the model parameters to a file called nbmodel.txt.

The classification program will be invoked in the following way:

> python nbclassify.py /path/to/input

The argument is the directory of the test data; the program will read the parameters of a naive Bayes model from the file nbmodel.txt, classify each file in the test data, and write the results to a text file called nboutput.txt in the following format:

label_a label_b path1
label_a label_b path2 

