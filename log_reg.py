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


def get_thresh(test_data, w):
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

	ac = np.array([])
	for thresh in np.linspace(0, 1, 101):
		true_positives = sum(i > thresh for i in good_builds)
		false_negatives = good_builds.shape[0] - true_positives
		true_negatives = sum(i <= thresh for i in failing_builds)
		false_positives = failing_builds.shape[0] - true_negatives
		accuracy = float(true_negatives + true_positives) / float(
			(good_builds.shape[0] + failing_builds.shape[0]))
		ac = np.append(ac, [accuracy])
	print("[")
	for i in ac:
		print(str(i) + ",")
	print("]")
	return ac


def train_classifier(training_data):
	kappa = 1.0
	w = np.zeros(5)

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


def evaluate_classifier(w, thresh, data):
	data = np.genfromtxt(data, delimiter=',')
	num_attributes = (data[0].shape[0] - 1)
	x_data = data[:, 0:num_attributes]
	y_data = data[:, num_attributes]
	dummy_col = np.ones((x_data.shape[0], 1))
	x_data = np.concatenate((dummy_col, x_data,), axis=1)
	ones = np.array([])
	negative_ones = np.array([])
	for i in range(0, y_data.shape[0]):
		sig = get_sigmoid_val(y_data[i], x_data[i], w)
		if (y_data[i] == 1.0):
			ones = np.append(ones, [sig])
		else:
			negative_ones = np.append(negative_ones, [sig])
	print(y_data.shape[0])
	true_positives = sum(i > thresh for i in ones)
	false_negatives = ones.shape[0] - true_positives
	true_negatives = sum(i <= thresh for i in negative_ones)
	false_positives = negative_ones.shape[0] - true_negatives
	a = np.array([true_negatives, false_positives, false_negatives, true_positives])
	print(a[0], a[1])
	print(a[2], a[3])
	print("")
	return a


def get_conf(w, thresh, file_list):
	a = np.zeros(4)
	for i in file_list:
		a += evaluate_classifier(np.array(w), thresh, i)
	print(a[0], a[1])
	print(a[2], a[3])


def main():
	NUM_ATTRIBUTES = 5
	# data = (['d0.csv', 'd1.csv', 'd2.csv', 'd3.csv', 'd4.csv', 'd5.csv', 'd6.csv', 'd7.csv', 'd8.csv', 'd9.csv'])
	# data = (['d0.csv'])
	# sys.stdout = open('roc.csv', 'w')
	data = (['d0_op.csv', 'd1_op.csv', 'd2_op.csv', 'd3_op.csv', 'd4_op.csv'])
	avg_w = np.zeros(NUM_ATTRIBUTES)
	ac = np.zeros(101)
	for d in data:
		print("TESTING", d)
		test_data = list(set(data) - set(d))
		w = train_classifier(test_data)
		avg_w += w
		ac += get_thresh(d, w)
	print(avg_w / len(data))

	ac = ac / 5
	get_conf(avg_w, 0.51 ,data)
	print("[")
	for i in ac:
		print(str(i) + ",")
	print("]")


main()
