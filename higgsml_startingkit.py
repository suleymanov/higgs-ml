print "This script trains a simple naive Bayes classifier"
print "and produces the submission file"

import random, string, math, csv
import numpy as np
import matplotlib.pyplot as plt

# import data
all = list(csv.reader(open("training.csv", "rb"), delimiter = ","))
xs = np.array([map(float, row[1:-2]) for row in all[1:]])
(numPoints, numFeatures) = xs.shape

# perturbing features to avoid ties. It's far from optimal
# but makes life easier in this simple example
xs = np.add(xs, np.random.normal(0.0, 0.0001, xs.shape))

# label selectors
sSelector = np.array([row[-1] == "s" for row in all[1:]])
bSelector = np.array([row[-1] == "b" for row in all[1:]])

# weights and weight sums
weights = np.array([float(row[-2]) for row in all[1:]])
sumWeights = np.sum(weights)
sumSWeights = np.sum(weights[sSelector])
sumBWeights = np.sum(weights[bSelector])

# training and validation cuts
randomPermutation = random.sample(range(len(xs)), len(xs))
numPointsTrain = int(numPoints * 0.9)
numPointsValidation = numPoints - numPointsTrain

xsTrain = xs[randomPermutation[:numPointsTrain]]
xsValidation = xs[randomPermutation[numPointsTrain:]]

sSelectorTrain = sSelector[randomPermutation[:numPointsTrain]]
bSelectorTrain = bSelector[randomPermutation[:numPointsTrain]]
sSelectorValidation = sSelector[randomPermutation[numPointsTrain:]]
bSelectorValidation = bSelector[randomPermutation[numPointsTrain:]]

weightsTrain = weights[randomPermutation[:numPointsTrain]]
weightsValidation = weights[randomPermutation[numPointsTrain:]]

sumWeightsTrain = np.sum(weightsTrain)
sumSWeightsTrain = np.sum(weightsTrain[sSelectorTrain])
sumBWeightsTrain = np.sum(weightsTrain[bSelectorTrain])

xsTrainTranspose = xsTrain.transpose()
weightsBalancedTrain = np.array([0.5 * weightsTrain[i] / sumSWeightsTrain
								if sSelectorTrain[i]
								else 0.5 * weightsTrain[i] / sumBWeightsTrain
								for i in range(numPointsTrain)])
								
# training naive Bayes and defining the score function
numBins = 10
logPs = np.empty([numFeatures, numBins])
binMaxs = np.empty([numFeatures, numBins])
binIndexes = np.array(range(0, numPointsTrain + 1, numPointsTrain / numBins))

for fI in range(numFeatures) :
	#index permutation of sorted feature column
	indexes = xsTrainTranspose[fI].argsort()
	for bI in range(numBins) :
		# upper bin limits
		binMaxs[fI, bI] = xsTrainTranspose[fI, indexes[binIndexes[bI + 1] - 1]]
		# training indices of points in a bin
		indexesInBin = indexes[binIndexes[bI]:binIndexes[bI + 1]]
		# sum of signal weights in bin
		wS = np.sum(weightsBalancedTrain[indexesInBin]
					[sSelectorTrain[indexesInBin]])
		# sum of background weights in bin
		wB = np.sum(weightsBalancedTrain[indexesInBin]
					[bSelectorTrain[indexesInBin]])
		# log probability of being a signal in the bin
		logPs[fI, bI] = math.log(wS / (wS + wB))
		
# score function used to sort test examples
def score(x) :
	logP = 0
	for fI in range(numFeatures) :
		bI = 0
		# linear search for the bin index of the fI-th feature
		# of the signal
		while bI < len(binMaxs[fI]) - 1 and x[fI] > binMaxs[fI, bI] :
			bI += 1
		logP += logPs[fI, bI] - math.log(0.5)
	return logP
	
# optimizing the AMS on the held out validation part
def AMS(s, b) :
	assert s >= 0
	assert b >= 0
	bReg = 10.
	return math.sqrt(2 * ((s + b + bReg) * math.log(1 + s / (b + bReg)) - s))
	
# computing the scores on the validation set
validationScores = np.array([score(x) for x in xsValidation])

# sorting the indices in increasing order of the scores
tIIs = validationScores.argsort()

# weights have to be normalized to the same sum as in the full set
wFactor = 1. * numPoints / numPointsValidation

# initializing s and b to the full sum of weights, we start by having
# all points in the selection region
s = np.sum(weightsValidation[sSelectorValidation])
b = np.sum(weightsValidation[bSelectorValidation])

# amss will contain AMSs after each point moved out of the selection region
# in the sorted validation set
amss = np.empty([len(tIIs)])

# amsMax will contain the best validation AMS, 
# and threshold will be the smallest score among the selected points
amsMax = 0
threshold = 0.0

# we will do len(tIIs) iterations, which means that amss[-1] is the AMS
# when only the point with the highest score is selected
for tI in range(len(tIIs)) :
	# don't forget to renormalize the weights to the same sum
	# as in the complete training set
	amss[tI] = AMS(max(0, s * wFactor), max(0, b * wFactor))
	if amss[tI] > amsMax :
		amsMax = amss[tI]
		threshold = validationScores[tIIs[tI]]
		# print tI, threshold
	if sSelectorValidation[tIIs[tI]] :
		s -= weightsValidation[tIIs[tI]]
	else :
		b -= weightsValidation[tIIs[tI]]
amsMax
threshold
plt.plot(amss)

# computing the permutation on the test set
test = list(csv.reader(open("test.csv", "rb"), delimiter = ","))
xsTest = np.array([map(float, row[1:]) for row in test[1:]])
testIds = np.array([int(row[0]) for row in test[1:]])

# computing the scores
testScores = np.array([score(x) for x in xsTest])

# computing the rank order
testInversePermutation = testScores.argsort()
testPermutation = list(testInversePermutation)
for tI, tII in zip(range(len(testInversePermutation)),
					testInversePermutation) :
	testPermutation[tII] = tI
	
# computing the submission file with columns EventId, RankOrder and Class
submission = np.array([[str(testIds[tI]), str(testPermutation[tI] + 1),
						's' if testScores[tI] >= threshold else 'b']
						for tI in range(len(testIds))])
submission = np.append([['EventId', 'RankOrder', 'Class']],
						submission, axis = 0)
						
# saving the file
np.savetxt("submission.csv", submission, fmt = "%s", delimiter = ",")