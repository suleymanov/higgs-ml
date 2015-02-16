import math, numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def logreg(X, y) :
	'''
		Logistic regression minimization using gradient descent.
		Takes X as matrix of features, y as binary income (0 or 1).
		Returns Theta - array of trained coefficients.
	'''
	(m, n) = X.shape
	Theta = np.zeros((1, n), float)
	iter = 500
	alpha = 0.5
	J_hist = np.zeros(iter)
	
	for i in range(iter) :
		Theta0 = np.array(Theta)
		tmp = np.dot(X, Theta0.transpose())
		h = np.array([[sigmoid(el)] for el in tmp])
		tmp2 = h - y
		tmp3 = np.dot(tmp2.transpose(), X)
		Theta -= (alpha / m) * tmp3
		J = Cost(X, y, Theta)
		J_hist[i] = J
		
	print "Plotting cost function values..."
	print "Best value found so far: " + str(J_hist[-1])
	plt.plot(J_hist)
	plt.grid(True)
	plt.show()
	
	return Theta
	
def logregBFGS(X, y, lam = 0) :
	''' Logistic regression minimization using scipy minimizer BFGS. '''
	(m, n) = X.shape
	Theta0 = np.zeros((1, n), float)
	res = minimize(Cost, Theta0, method = 'BFGS', jac = Cost_der, \
				   args = (X, y, lam), options = { 'disp' : True })
	return res.x
	
def Cost(Theta, X, y, lam = 0) :
	''' Logistic regression cost function. '''
	(m, n) = X.shape
	J = 0
	
	for i in range(m) :
		h = sigmoid(np.dot(X[i,:], Theta.transpose()))
		J -= (y[i] * math.log(h) + (1 - y[i]) * math.log(1 - h))
	
	J += (lam / 2.0) * np.dot(Theta[1:], Theta[1:].transpose())
	J /= m
	
	return J[0]
	
def Cost_der(Theta, X, y, lam = 0) :
	''' Logistic regression cost function derivatives. '''
	(m, n) = X.shape
	tmp = np.dot(X, Theta.transpose())
	h = np.array([[sigmoid(el)] for el in tmp])
	tmp2 = h - y
	tmp3 = np.dot(tmp2.transpose(), X)
	grad = (1. / m) * tmp3
	grad[0, 1:] += (lam / m) * Theta[1:]
	grad = np.ndarray.flatten(grad)
	return grad
	
def sigmoid(x) :
	return 1 / (1 + math.exp(-x))