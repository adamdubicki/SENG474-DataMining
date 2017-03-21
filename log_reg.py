import numpy as np
import math as m
import matplotlib.pyplot as plt
import time
import sys


def get_sigmoid_val(y, X, w):
	return float(1.0 / (1.0 + np.power(m.exp(1), -1 * np.dot(X, w.T))))


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
	# plt.show()
	most_accurate = [0, 2]

	ac = np.array([])
	for thresh in np.linspace(0, 1, 101):
		true_positives = sum(i > thresh for i in good_builds)
		false_negatives = good_builds.shape[0] - true_positives
		true_negatives = sum(i <= thresh for i in failing_builds)
		false_positives = failing_builds.shape[0] - true_negatives
		accuracy = float(true_negatives + true_positives) / float(
			(good_builds.shape[0] + failing_builds.shape[0]))
		ac = np.append(ac, [accuracy])

	# for thresh in np.linspace(0, 1, 101):
	# 	true_positives = sum(i > thresh for i in good_builds)
	# 	false_negatives = good_builds.shape[0] - true_positives
	# 	true_negatives = sum(i <= thresh for i in failing_builds)
	# 	false_positives = failing_builds.shape[0] - true_negatives
	# 	accuracy = float(true_negatives + true_positives) / float(
	# 		(good_builds.shape[0] + failing_builds.shape[0])) * 100.0
	# 	print(float(false_positives) / float(true_negatives + false_positives))
	print("true negatives", true_negatives, "false negatives", false_negatives)
	print("false positives", false_positives, "true positives", true_positives)
	print("[")
	for i in ac:
		print(str(i) + ",")
	print("]")
	return ac


def train_classifier(training_data):
	kappa = 1.0
	w = np.zeros(20)

	for i in range(0, 30):
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
	data = (['d0.csv', 'd1.csv', 'd2.csv', 'd3.csv', 'd4.csv', 'd5.csv', 'd6.csv', 'd7.csv', 'd8.csv', 'd9.csv'])
	# data = (['d0.csv'])
	sys.stdout = open('roc.csv', 'w')
	avg_w = np.zeros(20)
	ac = np.zeros(101)
	for d in data:
		print("TESTING", d)
		test_data = list(set(data) - set(d))
		w = train_classifier(test_data)
		avg_w += w
		ac += get_roc(d, w)
	print(avg_w / 10)
	ac = ac / 10
	for i in ac:
		print(str(i) + ",")
	print("]")


main()
