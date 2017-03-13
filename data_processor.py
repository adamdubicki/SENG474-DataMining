from datetime import date
from datetime import datetime


def get_class(test_passed, test_failed, build_passed):
	if (build_passed == 'failed' or build_passed == 'errored'):
		return -1
	else:
		test_passed = float(test_passed)
		total_tests = float(test_failed) + test_passed
		if (total_tests == 0.0):
			return 1
		else:
			if (float(test_passed / total_tests) >= 0.95):
				return 1
			else:
				return -1


def transform_data(line):
	transformation = []

	# Our dates are formatted as 2012 - 06 - 28 16:59:43
	date_format = '%Y-%m-%d %H:%M:%S'
	pure_attributes = list((set(range(2, 25))) - set([3, 17, 18, 19, 20, 21]))
	if 'NA' in line:
		return None
	else:
		# For logistic regression, when dealing with non-numeric data,
		# You must assign the classes to binary. so we will call ruby as 1
		# and java as 2. If we had three classes we would need 01, 10 , and 11 etc
		if (line[1] == 'ruby'):
			transformation.append(1)
		elif (line[1] == 'java'):
			transformation.append(0)

		# We can just straight up add all of the pure attributes
		for i in range(2, len(line)):
			if (i in pure_attributes):
				transformation.append(float((line[i])))

		# Convert the string dates to date and append the delta
		first_commit = datetime.strptime(line[3], date_format)
		build_at = datetime.strptime(line[18], date_format)
		delta = build_at - first_commit
		transformation.append(delta.days)

		# Whether the commit was done from the outside
		if(line[17] == 'TRUE'):
			transformation.append(1)
		else:
			transformation.append(0)

		# Get the class from the build status and tests
		transform_class = get_class(line[20], line[21], line[19])
		transformation.append(transform_class)
		print('')
	return transformation


file = open("data.csv")
line = file.readline()
print line
count = 0
while (count < 10000):
	line = file.readline().strip('\r\n').split(',')
	transform = transform_data(line)
	if (transform_data(line) != None):
		count += 1
		# print line
		print transform
