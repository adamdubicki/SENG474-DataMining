from datetime import date
from datetime import datetime
import time
import re


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
	pure_attributes = list((set(range(2, 17))) - set([3, 17]))
	if 'NA' in line:
		return None
	else:
		# [0] == is Ruby?
		if (line[1] == 'ruby'):
			transformation.append(1)
			transformation.append(0)
			transformation.append(0)
		# [1] == is Java?
		elif (line[1] == 'java'):
			transformation.append(0)
			transformation.append(1)
			transformation.append(0)
		# [2] == is Javascript?
		elif (line[1] == 'javascript'):
			transformation.append(0)
			transformation.append(0)
			transformation.append(1)

		# We can just straight up add all of the pure attributes
		# (2 -> 16) - 3
		for i in pure_attributes:
			transformation.append(float((line[i])))

		# Convert the string dates to date and append the delta
		first_commit = datetime.strptime(line[3], date_format)
		build_at = datetime.strptime(line[18], date_format)
		delta = build_at - first_commit
		if (delta.days < 0):
			transformation.append(0)
		else:
			transformation.append(delta.days)

		# Whether the commit was done from the outside
		if (line[17] == 'TRUE'):
			transformation.append(1)
		else:
			transformation.append(-1)

		# Get the class from the build status and tests
		transform_class = get_class(line[20], line[21], line[19])
		transformation.append(transform_class)

		return transformation


def get_data():
	f = open("data_synth.csv")
	f2 = open("output.csv", 'w')
	line = f.readline()
	count = 0
	startTime = time.time()
	print(": : : EXTRACTING DATA : : :")
	# Grab all of the attributes we want
	for line in f:
		line = line.strip('\r\n').split(',')
		transform = transform_data(line)
		if (transform_data(line) != None):
			count += 1
			f2.write(str(transform).strip('[,]') + "\n")
	print(": : : FINISHED EXTRACTING : : :")
	print("TIME: ", time.time() - startTime)
	return count


# NEED TO NORMALIZE ATTRIBUTES 3 -> 17
def normalize_data():
	f = open("output.csv")
	line = f.readline().strip('\n').split(',')
	normalized_attributes = range(3, 18)
	startTime = time.time()
	print(": : : NORMALIZING DATA : : :")

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
	print ("NORMALIZED ATTRIBUTE DATA", normalization_data)
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
		# ADD THE NOT NORMALIZED ATTRIBUTES BACK
		line[0] = float(line[0])
		line[1] = float(line[1])
		line[2] = float(line[2])
		line[18] = float(line[18])
		line[19] = float(line[19])
		if (line_count % 10 == 0):
			f0.write(str(line).strip('[,]') + "\n")
		elif (line_count % 10 == 1):
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
		line_count += 1
	print(": : : FINISHED NORMALIZING : : :")
	print("TIME: ", time.time() - startTime)


def create_files():
	string = "d0.csv"
	p = re.compile("\d")
	for i in range(11):
		open(string, 'a').close()
		string = p.sub(str(i), string)
	open("output.csv", 'a').close()


def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False


def get_data_with_nulls():
	f = open("data_synth.csv")
	f2 = open("output.csv", 'w')
	line = f.readline()
	print(line)
	count = 0
	startTime = time.time()

	normalized = range(1, 7)
	normalized_attributes = {}
	for i in normalized:
		normalized_attributes[i] = {'max': 0.0, 'min': 99999, 'sum': 0.0, 'not_null': 0.0}
	print(": : : EXTRACTING DATA : : :")

	for line in f:
		line = line.strip('\r\n').split(',')
		count += 1
		for attribute in normalized:
			if (line[attribute]) == 'NA' or line[attribute] == '':
				continue
			else:
				if (attribute not in [5, 6]):
					if float(line[attribute]) > normalized_attributes[attribute]['max']:
						normalized_attributes[attribute]['max'] = float(line[attribute])
					if float(line[attribute]) < normalized_attributes[attribute]['min']:
						normalized_attributes[attribute]['min'] = float(line[attribute])
					normalized_attributes[attribute]['sum'] += float(line[attribute])
					normalized_attributes[attribute]['not_null'] += 1
				if (attribute == 5):
					if (line[attribute] == 'TRUE'):
						normalized_attributes[attribute]['sum'] += 1
					normalized_attributes[attribute]['not_null'] += 1
				if (attribute == 6):
					if (line[attribute] == 'passed'):
						normalized_attributes[attribute]['sum'] += 1
					normalized_attributes[attribute]['not_null'] += 1

	f = open("data_synth.csv")
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
	line = f.readline()
	line_count = 0
	line_made = {}
	for line in f:
		new_line = []
		line = line.strip('\r\n').split(',')
		if (line[0] == 'ruby'):
			new_line.append(1)
			new_line.append(0)
			new_line.append(0)
		elif (line[0] == 'java'):
			new_line.append(0)
			new_line.append(1)
			new_line.append(0)
		else:
			new_line.append(0)
			new_line.append(0)
			new_line.append(1)
		for i in range(1, 5):
			new_val = line[i]
			avg = float(normalized_attributes[i]['sum'] / normalized_attributes[i]['not_null'])
			data_range = float(normalized_attributes[i]['max'] - normalized_attributes[i]['min'])
			if (new_val == 'NA' or new_val == '' or not isfloat(new_val)):
				new_line.append(0.0)
			else:
				new_line.append((float(new_val) - avg) / float(data_range))
		if (line[5] == 'TRUE'):
			new_line.append(1.0)
		else:
			new_line.append(0)
		if (line[6] == "passed"):
			new_line.append(1.0)
		else:
			new_line.append(-1.0)

		if(tuple(new_line) in line_made):
			pass
		else:
			line_made[tuple(new_line)] = 1
			if (line_count % 10 == 0):
				f0.write(str(new_line).strip('[,]') + "\n")
			elif (line_count % 10 == 1):
				f1.write(str(new_line).strip('[,]') + "\n")
			elif (line_count % 10 == 2):
				f2.write(str(new_line).strip('[,]') + "\n")
			elif (line_count % 10 == 3):
				f3.write(str(new_line).strip('[,]') + "\n")
			elif (line_count % 10 == 4):
				f4.write(str(new_line).strip('[,]') + "\n")
			elif (line_count % 10 == 5):
				f5.write(str(new_line).strip('[,]') + "\n")
			elif (line_count % 10 == 6):
				f6.write(str(new_line).strip('[,]') + "\n")
			elif (line_count % 10 == 7):
				f7.write(str(new_line).strip('[,]') + "\n")
			elif (line_count % 10 == 8):
				f8.write(str(new_line).strip('[,]') + "\n")
			elif (line_count % 10 == 9):
				f9.write(str(new_line).strip('[,]') + "\n")
			line_count += 1
			print line_count
	print (normalized_attributes)
	print(": : : FINISHED NORMALIZING : : :")
	print("TIME: ", time.time() - startTime)


# Grab all of the attributes we want
def main():
	# create_files()
	# get_data()
	# normalize_data()
	get_data_with_nulls()


main()
