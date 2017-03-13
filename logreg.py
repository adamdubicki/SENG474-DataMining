import numpy as np
import math as m


def get_sigmoid_val(x, w):
	return float(1 / (1.0 + m.exp(np.dot(x, w))))


def classify(x, w, thresh):
	sig = get_sigmoid_val(x, w)
	if (sig > thresh):
		return 1
	else:
		return 0


def compute_grad(x, y, w):
	# y .* X
	numerator = (y * x.T).T

	# 1 + e ** (y.*(X * w))
	denominator = np.ones(y.shape) + np.power(m.exp(1), (y * np.dot(x, w)))

	# SUM y.*X / (1 + e ** (y.*(X * w)))
	gradient = np.sum(np.divide(numerator.T, denominator).T, axis=0)

	return gradient


def train(kappa, x_data, y_data, w):
	for i in range(0, 100):
		w = np.add(w, float(kappa / y_data.shape[0]) * compute_grad(x_data, y_data, w))
	return w


def get_accuracy(w, x_data, y_data, thresh):
	correct = 0.0
	for i in range(0, y_data.shape[0]):
		guess = classify(x_data[i], w, thresh)
		if (guess == y_data[0]):
			correct += 1.0
	return float(correct / (y_data.shape[0] + 1))


def main():
	data = np.genfromtxt('a2_test_data.csv', delimiter=',')
	num_attributes = (data[0].shape[0] - 1)

	# Put data into form Xd = y
	x_data = data[:, 0:num_attributes]
	y_data = data[:, num_attributes]
	dummy_col = np.ones((x_data.shape[0], 1))
	x_data = np.concatenate((x_data, dummy_col), axis=1)

	# Create a zero w
	w = np.zeros(num_attributes + 1)

	# See how accurate our w is
	w = train(2.0, x_data, y_data, w)
	print(w)
	print(get_accuracy(w, x_data, y_data, 0.01))


main()
