import numpy as np
import math as m
import matplotlib.pyplot as plt


def get_sigmoid_val(y, X, w):
	return float(1.0 / ( 1.0 + np.power(m.exp(1), -1.0 * y * np.dot(X, w.T))))


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
	print ("Accuracy", float((tp+tn) / (y_data.shape[0])))
	return float((tp+tn) / (y_data.shape[0]))


def gradient_descent(y, X, w):
	numerator = ((y * X.T).T)
	denominator = np.ones(y.shape) + np.power(m.exp(1), y * np.dot(X, w.T))
	return 1.0 / y.shape[0] * (np.sum((numerator.T / denominator).T, axis=0))


def error(y, X, w):
	grad = np.log((np.ones(y.shape) + np.power(m.exp(1), -1.0 * y * np.dot(X, w.T))))
	return (1.0 / y.shape[0]) * np.sum(grad, axis=0)


def main():
	training_data = ['d1.csv', 'd2.csv', 'd3.csv', 'd4.csv', 'd5.csv', 'd6.csv','d7.csv','d8.csv', 'd9.csv']
	testing_data = 'd0.csv'
	kappa = 2.0
	w_accuracy = np.array([])

	w = np.zeros(20)
	# w = np.zeros(3)
	for i in range(0, 10):
		data = np.genfromtxt(testing_data, delimiter=',')
		num_attributes = (data[0].shape[0] - 1)
		x_data = data[:, 0:num_attributes]
		y_data = data[:, num_attributes]
		dummy_col = np.ones((x_data.shape[0], 1))
		x_data = np.concatenate((dummy_col, x_data,), axis=1)
		w_accuracy = np.append(w_accuracy, [get_accuracy(w, x_data, y_data, 0.5)])
		for t in training_data:
			data = np.genfromtxt(t, delimiter=',')
			num_attributes = (data[0].shape[0] - 1)
			x_data = data[:, 0:num_attributes]
			y_data = data[:, num_attributes]
			dummy_col = np.ones((x_data.shape[0], 1))
			x_data = np.concatenate((dummy_col, x_data,), axis=1)
			w = w + (kappa * (gradient_descent(y_data, x_data, w)))
	plt.plot(w_accuracy)
	plt.ylabel('Accuracy')
	plt.show()
	print(w)


main()
