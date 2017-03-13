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
		elif (line[1] == 'javascript'):
			transformation.append(2)
		else:
			print('Got something unexpected...', line[1])

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
		if (line[17] == 'TRUE'):
			transformation.append(1)
		else:
			transformation.append(0)

		# Get the class from the build status and tests
		transform_class = get_class(line[20], line[21], line[19])
		transformation.append(transform_class)

		return transformation


def get_data():
	f = open("data.csv")
	f2 = open("output.csv", 'w')
	f.readline()
	count = 0
	# Grab all of the attributes we want
	for line in f:
		line = line.strip('\r\n').split(',')
		transform = transform_data(line)
		if (transform_data(line) != None):
			count += 1
			f2.write(str(transform).strip('[,]') + "\n")
	return count


# NEED TO NORMALIZE ATTRIBUTES 1 -> 16
# 1, 2.0, 33.0, 2.0, 2.0, 0.0, 141.0, 0.0, 0.0, 5.0, 71.0, 17217.0, 639.426148574084, 73.9966312365685, 100.249753150955, 0, 0, 1
def normalize_data():
	f = open("output.csv")
	line = f.readline().strip('\n').split(',')
	normalized_attributes = range(1, 17)

	# Max at 0, Min at 1, Total at 2
	normalization_data = {}
	for i in normalized_attributes:
		normalization_data[i] = [float(line[i]), float(line[i]), float(line[i])]

	count = 0
	for line in f:
		line = line.strip('\n').split(',')
		count += 1
		for attribute in normalized_attributes:
			normalization_data[attribute][2] += float(line[attribute])
			if (float(line[attribute]) > normalization_data[attribute][0]):
				normalization_data[attribute][0] = float(line[attribute])
			if (float(line[attribute]) < normalization_data[attribute][1]):
				normalization_data[attribute][1] = float(line[attribute])

	f = open("output.csv")
	f0 = open("d0.csv", 'w')
	f1 = open("d1.csv", 'w')
	f2 = open("d2.csv", 'w')
	f3 = open("d3.csv", 'w')
	f4 = open("d4.csv", 'w')
	f5 = open("d5.csv", 'w')
	f6 = open("d6.csv", 'w')
	f7 = open("d7.csv", 'w')
	f8 = open("d8.csv", 'w')
	f9 = open("d9.csv", 'w')
	line_count = 0
	for line in f:
		line = line.strip('\n').split(',')
		for attribute in normalized_attributes:
			average = float((normalization_data[attribute][2]) / count)
			delta = float(normalization_data[attribute][0]) - float(normalization_data[attribute][1])
			line[attribute] = float(float(line[attribute]) - average) / delta
		line[0] = float(line[0])
		line[17] = float(line[17])
		if(line_count%10 == 0):
			f0.write(str(line).strip('[,]') + "\n")
		elif(line_count%10 == 1):
			f1.write(str(line).strip('[,]') + "\n")
		elif (line_count % 10 == 2):
			f2.write(str(line).strip('[,]') + "\n")
		elif (line_count % 10 == 3):
			f3.write(str(line).strip('[,]') + "\n")
		elif (line_count % 10 == 4):
			f4.write(str(line).strip('[,]') + "\n")
		elif (line_count % 10 == 5):
			f5.write(str(line).strip('[,]') + "\n")
		elif (line_count % 10 == 6):
			f6.write(str(line).strip('[,]') + "\n")
		elif (line_count % 10 == 7):
			f7.write(str(line).strip('[,]') + "\n")
		elif (line_count % 10 == 8):
			f8.write(str(line).strip('[,]') + "\n")
		elif (line_count % 10 == 9):
			f9.write(str(line).strip('[,]') + "\n")
		line_count +=1



def main():
	get_data()
	normalize_data()


main()
