# Print info
print "\nThis script performs logistic regression for signal/background detection"
print "in Higgs boson simulation data.\n"

# Read training data and divide to parts suitable for traiing
import csv, numpy as np

all_training = list(csv.reader(open("training.csv", "rb"), delimiter = ","))
h_training = all_training[0]
all_training = all_training[1:]

iid = h_training.index("EventId")
injet = h_training.index("PRI_jet_num")
ilabel = h_training.index("Label")

x_all = np.array([map(float, row[1:-2]) for row in all_training])
(numPoints, numFeatures) = x_all.shape

sSelector = np.array([row[-1] == "s" for row in all_training[1:]])
bSelector = np.array([row[-1] == "b" for row in all_training[1:]])

import break_data
break_data.break_data("training.csv", "training")
training_names = ["training (A).csv", "training (B).csv", "training (C).csv",
				  "training (D).csv", "training (E).csv", "training (F).csv"]

# Train logistic regression for each data subset


# Read test data and compute predictions
break_data.break_data("test.csv", "testing")

# Record results to submission file