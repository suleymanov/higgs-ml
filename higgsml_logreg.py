# Print info
print "\nThis script performs logistic regression for signal/background detection"
print "in Higgs boson simulation data.\n"

def AMS(s, b) :
	assert s >= 0
	assert b >= 0
	bReg = 10.
	return math.sqrt(2 * ((s + b + bReg) * math.log(1 + s / (b + bReg)) - s))

# Break train/test data files to make them suitable for training/testing
# (according to NA's structure in features)
import csv, numpy as np
import break_data, logreg_1_file

training_names = ["training (A).csv", "training (B).csv", "training (C).csv",
				  "training (D).csv", "training (E).csv", "training (F).csv"]
testing_names = ["testing (A).csv", "testing (B).csv", "testing (C).csv",
				 "testing (D).csv", "testing (E).csv", "testing (F).csv"]
				 
for train_file in training_names :
	if not os.path.exists(train_file) :
		break_data.break_data("training.csv", "training")
		break
		
for test_file in testing_names :
	if not os.path.exists(test_file) :
		break_data.break_data("testing.csv", "testing")
		break
		
# Train logistic regression for each data subset
cols_to_remove = [0, 23, 31, 32]
colsA = [j for j in range(33) if not j in cols_to_remove]
print "Performing logistic regression on A dataset"
print "\tExtracting data..."
events_A, X_A, weights_A, labels_A, y_A = extract_data(training_names[0], colsA)
print "\tFinished extracting data."
ThetaA = log_regression(X_A, y_A)

cols_to_remove = [0, 1, 23, 31, 32]
colsB = [j for j in range(33) if not j in cols_to_remove]
print "Performing logistic regression on B dataset"
print "\tExtracting data..."
events_B, X_B, weights_B, labels_B, y_B = extract_data(training_names[1], colsB)
print "\tFinished extracting data."
ThetaB = log_regression(X_B, y_B)

cols_to_remove = [0, 5, 6, 7, 13, 23, 27, 28, 29, 31, 32]
colsC = [j for j in range(33) if not j in cols_to_remove]
print "Performing logistic regression on C dataset"
print "\tExtracting data..."
events_C, X_C, weights_C, labels_C, y_C = extract_data(training_names[2], colsC)
print "\tFinished extracting data."
ThetaC = log_regression(X_C, y_C)

cols_to_remove = [0, 1, 5, 6, 7, 13, 23, 27, 28, 29, 31, 32]
colsD = [j for j in range(33) if not j in cols_to_remove]
print "Performing logistic regression on D dataset"
print "\tExtracting data..."
events_D, X_D, weights_D, labels_D, y_D = extract_data(training_names[3], colsD)
print "\tFinished extracting data."
ThetaD = log_regression(X_D, y_D)

cols_to_remove = [0, 5, 6, 7, 13, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
colsE = [j for j in range(33) if not j in cols_to_remove]
print "Performing logistic regression on E dataset"
print "\tExtracting data..."
events_E, X_E, weights_E, labels_E, y_E = extract_data(training_names[4], colsE)
print "\tFinished extracting data."
ThetaE = log_regression(X_E, y_E)

cols_to_remove = [0, 1, 5, 6, 7, 13, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
colsF = [j for j in range(33) if not j in cols_to_remove]
print "Performing logistic regression on F dataset"
print "\tExtracting data..."
events_F, X_F, weights_F, labels_F, y_F = extract_data(training_names[5], colsF)
print "\tFinished extracting data."
ThetaF = log_regression(X_F, y_F)

# Read test data and compute predictions


# Sort and record results to submission file
