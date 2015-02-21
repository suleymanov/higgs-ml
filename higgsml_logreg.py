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
import os, csv, numpy as np
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
cols_to_remove = [0, 1, 23, 31, 32]
colsB = [j for j in range(33) if not j in cols_to_remove]
cols_to_remove = [0, 5, 6, 7, 13, 23, 27, 28, 29, 31, 32]
colsC = [j for j in range(33) if not j in cols_to_remove]
cols_to_remove = [0, 1, 5, 6, 7, 13, 23, 27, 28, 29, 31, 32]
colsD = [j for j in range(33) if not j in cols_to_remove]
cols_to_remove = [0, 5, 6, 7, 13, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
colsE = [j for j in range(33) if not j in cols_to_remove]
cols_to_remove = [0, 1, 5, 6, 7, 13, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
colsF = [j for j in range(33) if not j in cols_to_remove]

skip_training = True

if not skip_training :
	print "Performing logistic regression on A dataset"
	print "\tExtracting data..."
	events_A, X_A, weights_A, labels_A, y_A = logreg_1_file.extract_data \
											(training_names[0], colsA)
	print "\tFinished extracting data."
	ThetaA = logreg_1_file.log_regression(X_A, y_A)

	print "Performing logistic regression on B dataset"
	print "\tExtracting data..."
	events_B, X_B, weights_B, labels_B, y_B = logreg_1_file.extract_data \
											(training_names[1], colsB)
	print "\tFinished extracting data."
	ThetaB = logreg_1_file.log_regression(X_B, y_B)

	print "Performing logistic regression on C dataset"
	print "\tExtracting data..."
	events_C, X_C, weights_C, labels_C, y_C = logreg_1_file.extract_data \
											(training_names[2], colsC)
	print "\tFinished extracting data."
	ThetaC = logreg_1_file.log_regression(X_C, y_C)

	print "Performing logistic regression on D dataset"
	print "\tExtracting data..."
	events_D, X_D, weights_D, labels_D, y_D = logreg_1_file.extract_data \
											(training_names[3], colsD)
	print "\tFinished extracting data."
	ThetaD = logreg_1_file.log_regression(X_D, y_D)

	print "Performing logistic regression on E dataset"
	print "\tExtracting data..."
	events_E, X_E, weights_E, labels_E, y_E = logreg_1_file.extract_data \
											(training_names[4], colsE)
	print "\tFinished extracting data."
	ThetaE = logreg_1_file.log_regression(X_E, y_E)

	print "Performing logistic regression on F dataset"
	print "\tExtracting data..."
	events_F, X_F, weights_F, labels_F, y_F = logreg_1_file.extract_data \
											(training_names[5], colsF)
	print "\tFinished extracting data."
	ThetaF = logreg_1_file.log_regression(X_F, y_F)
	
	np.savetxt("ThetaA.csv", ThetaA, fmt = "%s", delimiter = ",")
	np.savetxt("ThetaB.csv", ThetaB, fmt = "%s", delimiter = ",")
	np.savetxt("ThetaC.csv", ThetaC, fmt = "%s", delimiter = ",")
	np.savetxt("ThetaD.csv", ThetaD, fmt = "%s", delimiter = ",")
	np.savetxt("ThetaE.csv", ThetaE, fmt = "%s", delimiter = ",")
	np.savetxt("ThetaF.csv", ThetaF, fmt = "%s", delimiter = ",")
else :
	data = list(csv.reader(open("ThetaA.csv", "rb"), delimiter = ","))
	ThetaA = (np.array([map(float, row) for row in data])).transpose()
	data = list(csv.reader(open("ThetaB.csv", "rb"), delimiter = ","))
	ThetaB = (np.array([map(float, row) for row in data])).transpose()
	data = list(csv.reader(open("ThetaC.csv", "rb"), delimiter = ","))
	ThetaC = (np.array([map(float, row) for row in data])).transpose()
	data = list(csv.reader(open("ThetaD.csv", "rb"), delimiter = ","))
	ThetaD = (np.array([map(float, row) for row in data])).transpose()
	data = list(csv.reader(open("ThetaE.csv", "rb"), delimiter = ","))
	ThetaE = (np.array([map(float, row) for row in data])).transpose()
	data = list(csv.reader(open("ThetaF.csv", "rb"), delimiter = ","))
	ThetaF = (np.array([map(float, row) for row in data])).transpose()

# Compute AMS score on train data

	
# Read test data and compute predictions
print "Computing score on A test dataset"
print "\tExtracting data..."
events_A, X_A_test = logreg_1_file.extract_data(testing_names[0], colsA, True)
X_A_test = logreg_1_file.scale_features(X_A_test)
print "\tFinished extracting data."
A_probs = logreg_1_file.eval_probs(X_A_test, ThetaA)

print "Computing score on B test dataset"
print "\tExtracting data..."
events_B, X_B_test = logreg_1_file.extract_data(testing_names[1], colsB, True)
X_B_test = logreg_1_file.scale_features(X_B_test)
print "\tFinished extracting data."
B_probs = logreg_1_file.eval_probs(X_B_test, ThetaB)

print "Computing score on C test dataset"
print "\tExtracting data..."
events_C, X_C_test = logreg_1_file.extract_data(testing_names[2], colsC, True)
X_C_test = logreg_1_file.scale_features(X_C_test)
print "\tFinished extracting data."
C_probs = logreg_1_file.eval_probs(X_C_test, ThetaC)

print "Computing score on D test dataset"
print "\tExtracting data..."
events_D, X_D_test = logreg_1_file.extract_data(testing_names[3], colsD, True)
X_D_test = logreg_1_file.scale_features(X_D_test)
print "\tFinished extracting data."
D_probs = logreg_1_file.eval_probs(X_D_test, ThetaD)

print "Computing score on E test dataset"
print "\tExtracting data..."
events_E, X_E_test = logreg_1_file.extract_data(testing_names[4], colsE, True)
X_E_test = logreg_1_file.scale_features(X_E_test)
print "\tFinished extracting data."
E_probs = logreg_1_file.eval_probs(X_E_test, ThetaE)

print "Computing score on F test dataset"
print "\tExtracting data..."
events_F, X_F_test = logreg_1_file.extract_data(testing_names[5], colsF, True)
X_F_test = logreg_1_file.scale_features(X_F_test)
print "\tFinished extracting data."
F_probs = logreg_1_file.eval_probs(X_F_test, ThetaF)

# Collect results, sort and record to submission file
A_data = np.concatenate((events_A, A_probs), axis = 1)
B_data = np.concatenate((events_B, B_probs), axis = 1)
C_data = np.concatenate((events_C, C_probs), axis = 1)
D_data = np.concatenate((events_D, D_probs), axis = 1)
E_data = np.concatenate((events_E, E_probs), axis = 1)
F_data = np.concatenate((events_F, F_probs), axis = 1)

all_data = np.concatenate((A_data, B_data, C_data, D_data, E_data, F_data), \
							axis = 0)

np.savetxt("all data.csv", all_data, fmt = "%s", delimiter = ",")
inds = all_data[:, 1].argsort()
						
print "Creating submission file..."					
submission = np.array([[str(int(all_data[inds[i], 0])), str(i + 1), \
					"s" if all_data[i, 1] >= 0.5 else "b"] \
					for i in range(all_data.shape[0])])
					
submission = np.append([['EventId', 'RankOrder', 'Class']],
						submission, axis = 0)
np.savetxt("submission.csv", submission, fmt = "%s", delimiter = ",")