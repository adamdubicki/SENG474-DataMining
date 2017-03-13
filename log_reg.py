import numpy as np
import math as m


def get_sigmoid_val(x, w, y):
	val = float(1 / (1 + np.power(m.exp(1), (-1.0 * y * np.dot(x, w)))))
	print val
	return val


def classify(x, w, thresh, y):
	sig = get_sigmoid_val(x, w, y)
	if (sig > thresh):
		return 1.0
	else:
		return -1.0


def compute_grad(x, y, w):
	# y .* X
	numerator = (y * x.T).T

	# 1 + e ** (y.*(X * w))
	denominator = np.ones(y.shape) + np.power(m.exp(1), (y * np.dot(x, w)))

	# SUM y.*X / (1 + e ** (y.*(X * w)))
	gradient = np.sum(np.divide(numerator.T, denominator).T, axis=0)

	return gradient


def train(kappa, x_data, y_data, w):
	w = np.add(w, float(kappa / y_data.shape[0]) * compute_grad(x_data, y_data, w))
	return w


def get_accuracy(w, x_data, y_data, thresh):
	correct = 0.0
	for i in range(0, y_data.shape[0]):
		guess = classify(x_data[i], w, thresh, y_data[i])
		print("GUESSED: " + str(guess) + "    ACTUAL:" + str(y_data[i]))
		if (guess == y_data[i]):
			print (guess, '==', y_data[i])
			correct += 1.0
	print "Got " + str(correct) + " many correct out of " + str(y_data.shape[0] + 1)
	return float(correct / (y_data.shape[0] + 1))


def main():
	training_data = ['d1.csv', 'd2.csv', 'd3.csv', 'd4.csv', 'd5.csv', 'd6.csv', 'd7.csv', 'd8.csv', 'd9.csv']
	testing_data = ['d0.csv']

	w = np.zeros(18)

	for i in range(0, 10):
		for t in training_data:
			data = np.genfromtxt(t, delimiter=',')
			num_attributes = (data[0].shape[0] - 1)
			x_data = data[:, 0:num_attributes]
			y_data = data[:, num_attributes]
			dummy_col = np.ones((x_data.shape[0], 1))
			x_data = np.concatenate((x_data, dummy_col), axis=1)
			w = train(2.0, x_data, y_data, w)
		print("FINISHED ROUND ", i)
	print w

	data = np.genfromtxt('d0.csv', delimiter=',')
	num_attributes = (data[0].shape[0] - 1)
	x_data = data[:, 0:num_attributes]
	y_data = data[:, num_attributes]
	dummy_col = np.ones((x_data.shape[0], 1))
	x_data = np.concatenate((x_data, dummy_col), axis=1)
	print("ACCURACY: ", str(get_accuracy(w, x_data, y_data, 0.4) * 100) + '%')


# data = np.genfromtxt('d1.csv', delimiter=',')
# num_attributes = (data[0].shape[0] - 1)
#
# # Put data into form Xd = y
# x_data = data[:, 0:num_attributes]
# y_data = data[:, num_attributes]
# dummy_col = np.ones((x_data.shape[0], 1))
# x_data = np.concatenate((x_data, dummy_col), axis=1)
#
# # Create a zero w
# w = np.zeros(num_attributes + 1)
#
# # See how accurate our w is
# w = train(2.0, x_data, y_data, w)
# print("ACCURACY: ", str(get_accuracy(w, x_data, y_data, 0.4)*100) + '%')


main()
