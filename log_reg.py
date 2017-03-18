import numpy as np
import math as m
import matplotlib.pyplot as plt
import time


def get_sigmoid_val(y, X, w):
	return float(1.0 / (1.0 + np.power(m.exp(1),  -1 * np.dot(X, w.T))))


def get_accuracy(w, x_data, y_data, thresh):
	correct = 0.0
	p = 0.0
	n = 0.0
	tp = 0.0
	fp = 0.0
	tn = 0.0
	fn = 0.0
	good_builds = np.array([])
	failing_builds = np.array([])

	for i in range(0, y_data.shape[0]):
		sig = get_sigmoid_val(y_data[i], x_data[i], w)
		# print(sig, y_data[i])
		if sig > thresh:
			good_builds = np.append(good_builds, [sig])
			guess = 1.0
		else:
			failing_builds = np.append(failing_builds, [sig])
			guess = -1.0

		if (y_data[i] == 1):
			p += 1.0
		else:
			n += 1.0

		if (guess == y_data[i]):
			correct += 1.0
			if guess == 1.0:
				tp += 1.0
			else:
				tn += 1.0
		else:
			if (guess == 1.0):
				fp += 1.0
			else:
				fn += 1.0

	print ("Positives:", p)
	print ("Negatives:", n)
	print ("True Positives", tp)
	print ("True Negatives", tn)
	print ("False Positives", fp)
	print ("False Negatives", fn)
	print ("Accuracy", float((tp + tn) / (y_data.shape[0])))
	# plt.plot(good_builds, good_builds, 'r')
	# plt.plot(failing_builds, failing_builds, 'b')
	# plt.show()
	return float((tp + tn) / (y_data.shape[0]))


def gradient_descent(y, X, w):
	numerator = ((y * X.T).T)
	denominator = np.ones(y.shape) + np.power(m.exp(1), y * np.dot(X, w.T))
	return 1.0 / y.shape[0] * (np.sum((numerator.T / denominator).T, axis=0))


def error(y, X, w):
	grad = np.log((np.ones(y.shape) + np.power(m.exp(1), -1.0 * y * np.dot(X, w.T))))
	return (1.0 / y.shape[0]) * np.sum(grad, axis=0)


def get_roc(test_data, w):
	data = np.genfromtxt(test_data, delimiter=',')
	num_attributes = (data[0].shape[0] - 1)
	x_data = data[:, 0:num_attributes]
	y_data = data[:, num_attributes]
	dummy_col = np.ones((x_data.shape[0], 1))
	x_data = np.concatenate((dummy_col, x_data,), axis=1)

	good_builds = np.array([])
	failing_builds = np.array([])
	for i in range(0, y_data.shape[0]):
		sig = get_sigmoid_val(y_data[i], x_data[i], w)
		if (y_data[i] == 1.0):
			good_builds = np.append(good_builds, [sig])
		else:
			failing_builds = np.append(failing_builds, [sig])

	good_builds.sort()
	failing_builds.sort()
	plt.plot(np.ones(good_builds.shape[0]), good_builds, 'r')
	plt.plot(-1 * np.ones(failing_builds.shape[0]), failing_builds, 'b')
	plt.show()
	print(good_builds)
	print(failing_builds)


def train_classifier(training_data):
	kappa = 2.0
	w = np.zeros(9)

	for i in range(0, 10):
		for t in training_data:
			data = np.genfromtxt(t, delimiter=',')
			num_attributes = (data[0].shape[0] - 1)
			x_data = data[:, 0:num_attributes]
			y_data = data[:, num_attributes]
			dummy_col = np.ones((x_data.shape[0], 1))
			x_data = np.concatenate((dummy_col, x_data,), axis=1)
			w = w + (kappa * (gradient_descent(y_data, x_data, w)))
	print w
	return w


def main():
	# Train w on a training set
	# w = train_classifier(['d0.csv', 'd1.csv', 'd2.csv', 'd3.csv', 'd4.csv', 'd5.csv', 'd6.csv', 'd7.csv', 'd8.csv'])
	# Or just use a w to get roc quicker
	w = np.array(
		[[0.45339011, 0.12258675, 0.28721841, 0.04358495, -0.0526, -0.13355728, -0.00250463, -0.01697852, 0.33722971]])
	get_roc('d0.csv', w)

main()
