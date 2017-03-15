import numpy as np
import math as m
import matplotlib.pyplot as plt


def get_sigmoid_val(x, w, y):
	val = float(1 / (1 + np.power(m.exp(1), (-1.0 * y * np.dot(x, w)))))
	return val


def classify(x, w, thresh, y):
	sig = get_sigmoid_val(x, w, y)
	if sig > thresh:
		return 1.0
	else:
		return -1.0


def compute_grad(x, y, w):
	numerator = (y * x.T).T
	denominator = np.ones(y.shape) + np.power(m.exp(1), (y * np.dot(x, w)))
	gradient = np.sum(np.divide(numerator.T, denominator).T, axis=0)
	return gradient


def train(kappa, x_data, y_data, w):
	w = np.add(w, float(kappa / y_data.shape[0]) * compute_grad(x_data, y_data, w))
	return w


def get_accuracy(w, x_data, y_data, thresh):
	correct = 0.0
	p = 0.0
	n = 0.0
	tp = 0.0
	fp = 0.0
	tn = 0.0
	fn = 0.0

	for i in range(0, y_data.shape[0]):
		guess = classify(x_data[i], w, thresh, y_data[i])
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
	print ("Accuracy", float(correct / (y_data.shape[0])))
	return float(correct / (y_data.shape[0]))


def main():

	testing_data = 'd0.csv'
	training_data = ['d1.csv', 'd2.csv', 'd3.csv', 'd4.csv', 'd5.csv', 'd6.csv', 'd7.csv', 'd8.csv', 'd9.csv']
	# training_data = ['d0.csv']
	w = np.zeros(20)
	accuracy = np.array([])

	for i in range(0, 10):
		print "\n: : : NEW ROUND : : :\n"
		data = np.genfromtxt(testing_data, delimiter=',')
		num_attributes = (data[0].shape[0] - 1)
		x_data = data[:, 0:num_attributes]
		y_data = data[:, num_attributes]
		dummy_col = np.ones((x_data.shape[0], 1))
		x_data = np.concatenate((x_data, dummy_col), axis=1)
		accuracy = np.append(accuracy, [get_accuracy(w, x_data, y_data, 0.5) * 100])
		for t in training_data:
			data = np.genfromtxt(t, delimiter=',')
			num_attributes = (data[0].shape[0] - 1)
			x_data = data[:, 0:num_attributes]
			y_data = data[:, num_attributes]
			dummy_col = np.ones((x_data.shape[0], 1))
			x_data = np.concatenate((x_data, dummy_col), axis=1)
			w = train(0.01, x_data, y_data, w)
	print w
	plt.plot(accuracy)
	plt.ylabel('Accuracy %')
	plt.show()


main()
