# This file impleents Point-biserial correlation coefficient as described here:
# https://en.wikipedia.org/wiki/Point-biserial_correlation_coefficient
# It's mathematically equivalent to the widely used Pearson correlation

import csv
import math
import numpy as np
import sys

# From stack overflow because header fields were giving me some issues
maxInt = sys.maxsize
decrement = True

while decrement:
	# decrease the maxInt value by factor 10
	# as long as the OverflowError occurs.

	decrement = False
	try:
		csv.field_size_limit(maxInt)
	except OverflowError:
		maxInt = int(maxInt/10)
		decrement = True

file = open("travistorrent_8_2_2017.csv")
src = "git_diff_src_churn"
result = "tr_status"

# Make lists of passed, failed and total numbers of the attribute
passed = []
failed = []
total = []

# Get the file's lables
labels = file.readline()
labels = labels.split(',')

for i in range(len(labels)):
	labels[i] = labels[i].strip("\"")

count = 0
for word in labels:
	if word == src:
		src = count
	if word == result:
		result = count
	count += 1


reader = csv.reader(file)

for line in reader:
	if float(line[src]) > 1000:
		continue
	if line[result] == "passed":
		passed.append(line[src])
	else:
		failed.append(line[src])
	total.append(line[src])

passed = np.array(passed).astype(np.float)
failed = np.array(failed).astype(np.float)
total = np.array(total).astype(np.float)

passed_mean = passed.mean()#np.mean(passed)
failed_mean = failed.mean()#np.mean(failed)

# This is standard standard deviation and not population standard deviation
std = np.std(total, ddof=1)
otherpart = math.sqrt(float((len(passed) * len(failed))) / float((len(total) * (len(total) - 1))))

correlation = ((passed_mean - failed_mean) / std) * otherpart

print correlation
