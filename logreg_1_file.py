if __name__ == '__main__' :
	print "\nThis script performs logistic regression on single file\n"

import csv, os, random, sys, numpy as np
import logreg

def scale_features(X) :
	(m, n) = X.shape
	for j in range(n) :
		minj = min(X[:, j])
		maxj = max(X[:, j])
		X[:, j] = (X[:, j] - minj) / (maxj - minj)
	return X
		
def score(X, y, Theta) :
	(m, n) = X.shape
	count = 0
	probs = [logreg.sigmoid(np.dot(X[i, :], Theta.transpose())) for i in range(m)]
	pred = np.array([1 if prob >= 0.5 else 0 for prob in probs], int)
	for i in range(len(pred)) :
		if y[i] == pred[i] :
			count += 1
	return 1.0 * count / (1.0 * m) * 100.0, probs
	
def extract_data(filename, cols, test = False) :
	assert os.path.exists(filename)
	data = list(csv.reader(open(filename, "rb"), delimiter = ","))
	X = np.array([map(float, [row[j] for j in cols]) for row in data[1:]])
	# events = np.array([map(int, row[0] for row in data[1:])])
	# weights = np.array([map(float, row[-2] for row in data[1:])])
	# events = np.array([map(int, row[0]) for row in data[1:]])
	# weights = np.array([map(float, row[-2]) for row in data[1:]])
	events = np.array([int(row[0]) for row in data[1:]])
	if not test :
		weights = np.array([float(row[-2]) for row in data[1:]])
		labels = [row[-1] for row in data[1:]]
		y = np.array([[1 if label == "s" else 0 for label in labels]]).transpose()
		return events, X, weights, labels, y
	else :
		return events, X
	
def log_regression(X, y) :
	(num_ex, num_f) = X.shape
	X = scale_features(X)
	random_permute = random.sample(range(num_ex), num_ex)
	num_train = int(num_ex * 0.9)
	num_validation = num_ex - num_train
	X_train = X[random_permute[:num_train], :]
	y_train = y[random_permute[:num_train]]
	X_validation = X[random_permute[num_train:], :]
	y_validation = y[random_permute[num_train:]]
	Theta = logreg.logregBFGS(X_train, y_train)
	score_training = score(X_train, y_train, Theta)
	score_validation = score(X_validation, y_validation, Theta)
	print "Score on training data = " + str(score_training)
	print "Score on validation data = " + str(score_validation)
	return Theta
	
# def log_regression(filename, cols) :
	# assert os.path.exists(filename)
	# data = list(csv.reader(open(filename, "rb"), delimiter = ","))
	# X = np.array([map(float, [row[j] for j in cols]) for row in data[1:]])
	# (num_ex, num_f) = X.shape
	# labels = [row[-1] for row in data[1:]]
	# y = np.array([[1 if label == "s" else 0 for label in labels]]).transpose()
	# X = scale_features(X) # scale features to have them in [0, 1] range
	# random_permute = random.sample(range(num_ex), num_ex)
	# num_train = int(num_ex * 0.9)
	# num_validation = num_ex - num_train
	# X_train = X[random_permute[:num_train], :]
	# y_train = y[random_permute[:num_train]]
	# X_validation = X[random_permute[num_train:], :]
	# y_validation = y[random_permute[num_train:]]
	# Theta = logreg.logregBFGS(X_train, y_train)
	# score_training = score(X_train, y_train, Theta)
	# score_validation = score(X_validation, y_validation, Theta)
	# print "Score on training data = " + str(score_training)
	# print "Score on validation data = " + str(score_validation) + "\n"
	# return Theta
	
# for testing
if __name__ == '__main__' :
	# break_data(sys.argv[1], sys.argv[2])
	
	# A set contains only defined values
	training_f = "training (A).csv"
	cols_to_remove = [0, 23, 31, 32]
	cols = [j for j in range(33) if not j in cols_to_remove]
	print "Performing logistic regression on A dataset"
	events, X, weights, labels, y = extract_data(training_f, cols)
	# Theta = log_regression(training_f, cols)
	Theta = log_regression(X, y)
	
	# B set shouldn't contain "DER_mass_MMC" (1) column
	training_f = "training (B).csv"
	cols_to_remove = [0, 1, 23, 31, 32]
	cols = [j for j in range(33) if not j in cols_to_remove]
	print "Performing logistic regression on B dataset"
	events, X, weights, labels, y = extract_data(training_f, cols)
	# Theta = log_regression(training_f, cols)
	Theta = log_regression(X, y)
	
	# C set shouldn't contain "DER_deltaeta_jet_jet" (5) column
	# AND, as well, "DER_mass_jet_jet" (6), "DER_prodeta_jet_jet" (7), 
	# "DER_lep_eta_centrality" (13), "PRI_jet_subleading_pt" (27),
	# "PRI_jet_subleading_eta" (28) and "PRI_jet_subleading_phi" (29) columns
	training_f = "training (C).csv"
	cols_to_remove = [0, 5, 6, 7, 13, 23, 27, 28, 29, 31, 32]
	cols = [j for j in range(33) if not j in cols_to_remove]
	print "Performing logistic regression on C dataset"
	events, X, weights, labels, y = extract_data(training_f, cols)
	# Theta = log_regression(training_f, cols)
	Theta = log_regression(X, y)
	
	# D set shouldn't contain "DER_mass_MMC" and "DER_deltaeta_jet_jet" columns
	training_f = "training (D).csv"
	cols_to_remove = [0, 1, 5, 6, 7, 13, 23, 27, 28, 29, 31, 32]
	cols = [j for j in range(33) if not j in cols_to_remove]
	print "Performing logistic regression on D dataset"
	events, X, weights, labels, y = extract_data(training_f, cols)
	# Theta = log_regression(training_f, cols)
	Theta = log_regression(X, y)
	
	# E set shouldn't contain "DER_deltaeta_jet_jet" and 
	# "PRI_jet_leading_pt" (24) columns, AND, as well, 
	# "PRI_jet_leading_eta" (25) and "PRI_jet_leading_phi" (26) columns
	# (and "PRI_jet_all_pt", because for this case it's all gonna be 0)
	training_f = "training (E).csv"
	cols_to_remove = [0, 5, 6, 7, 13, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
	cols = [j for j in range(33) if not j in cols_to_remove]
	print "Performing logistic regression on E dataset"
	events, X, weights, labels, y = extract_data(training_f, cols)
	# Theta = log_regression(training_f, cols)
	Theta = log_regression(X, y)
	
	# F set shouldn't contain "DER_mass_MMC", "DER_deltaeta_jet_jet" and
	# "PRI_jet_leading_pt" columns
	# (and "PRI_jet_all_pt", because for this case it's all gonna be 0)
	training_f = "training (F).csv"
	cols_to_remove = [0, 1, 5, 6, 7, 13, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
	cols = [j for j in range(33) if not j in cols_to_remove]
	print "Performing logistic regression on F dataset"
	events, X, weights, labels, y = extract_data(training_f, cols)
	# Theta = log_regression(training_f, cols)
	Theta = log_regression(X, y)