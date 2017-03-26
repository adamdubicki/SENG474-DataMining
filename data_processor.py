from datetime import date
from datetime import datetime
import time
import re
import numpy as np


def get_class(build_passed):
	if (build_passed == 'failed' or build_passed == 'errored'):
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
		transform_class = get_class(line[20])
		transformation.append(transform_class)

		return transformation


def get_data():
	f = open("data.csv")
	f2 = open("output.csv", 'w')
	line = f.readline()
	count = 0
	print (line.split(','))
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
	negative_count = 0
	positive_count = 0
	print(line)
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
	print(count)
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
	line_made = {}
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
		if (False):
			pass
		else:
			if ((line[19] == -1)):
				negative_count += 1
			else:
				positive_count += 1
			line_made[tuple(line)] = 1
			if ((negative_count < 5000 and line[19] == -1) or (positive_count < 5000 and line[19] == 1)):
				f0.write(str(line).strip('[,]') + "\n")
			elif ((negative_count < 10000 and line[19] == -1) or (positive_count < 10000 and line[19] == 1)):
				f1.write(str(line).strip('[,]') + "\n")
			elif ((negative_count < 15000 and line[19] == -1) or (positive_count < 15000 and line[19] == 1)):
				f2.write(str(line).strip('[,]') + "\n")
			elif ((negative_count < 20000 and line[19] == -1) or (positive_count < 20000 and line[19] == 1)):
				f3.write(str(line).strip('[,]') + "\n")
			elif ((negative_count < 25000 and line[19] == -1) or (positive_count < 25000 and line[19] == 1)):
				f4.write(str(line).strip('[,]') + "\n")
			elif ((negative_count < 30000 and line[19] == -1) or (positive_count < 30000 and line[19] == 1)):
				f5.write(str(line).strip('[,]') + "\n")
			elif ((negative_count < 35000 and line[19] == -1) or (positive_count < 35000 and line[19] == 1)):
				f6.write(str(line).strip('[,]') + "\n")
			elif ((negative_count < 45000 and line[19] == -1) or (positive_count < 45000 and line[19] == 1)):
				f7.write(str(line).strip('[,]') + "\n")
			elif ((negative_count < 50000 and line[19] == -1) or (positive_count < 50000 and line[19] == 1)):
				f8.write(str(line).strip('[,]') + "\n")
			elif ((negative_count < 55000 and line[19] == -1) or (positive_count < 55000 and line[19] == 1)):
				f9.write(str(line).strip('[,]') + "\n")
			line_count += 1
	print("POSITIVES", positive_count)
	print("NEGATIVES", negative_count)
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


# gh_first_commit_created_at,[0]
# gh_num_commits_in_push, [1]
# git_diff_src_churn, [2]
# gh_by_core_team_member, [3]
# gh_diff_files_modified, [4]
# gh_build_started_at, [5]
# tr_status [6]
# 9.0, 2.0, 0.0, 1.0, 95, -1
def process_op_data():
	f = open("op_data.csv")
	line = f.readline().strip('\n').split(',')
	startTime = time.time()
	negative_count = 0
	positive_count = 0
	print(line)

	# Max at 0, Min at 1, Total at 2
	data = []
	date_format = '%Y-%m-%dT%H:%M:%S'
	for line in f:
		line = line.strip('\n').split(',')
		new_line = []
		new_line.append(float(line[1])/1000)
		new_line.append(float(line[2])/1000)
		if(line[3] == 'TRUE'):
			new_line.append(1.0)
		else:
			new_line.append(0.0)
		# new_line.append(float(line[4])/1000)
		if(line[0] != '' and line[5] != ''):
			first_commit = datetime.strptime(line[0], date_format)
			build_at = datetime.strptime(line[5], date_format)
			delta = build_at - first_commit
			if (delta.days < 0):
				new_line.append(0)
			else:
				new_line.append(float(delta.days)/1000)
		else:
			new_line.append(0.0)
		data_class = get_class(line[6])
		if(data_class == 1):
			positive_count +=1
		else:
			negative_count +=1
		new_line.append(data_class)
		data.append(new_line)

	normalization_data = {}
	for i in [0,1,3]:
		normalization_data[i] = [float(data[0][i]), float(data[0][i]), float(data[0][i])]
	for attribute in data:
		for i in [0, 1, 3]:
			normalization_data[i][2]+=attribute[i]
			if(attribute[i]>normalization_data[i][0]):
				normalization_data[i][0] = attribute[i]
			if (attribute[i] < normalization_data[i][1]):
				normalization_data[i][1] = attribute[i]
	print(normalization_data)
	for i in range(len(data)):
		for attribute in [0,1,3]:
			average = float((normalization_data[attribute][2]) / 10000)
			delta = float(normalization_data[attribute][0]) - float(normalization_data[attribute][1])
			data[i][attribute] = float(float(data[i][attribute]) - average) / delta
	f0 = open("d0_op.csv", 'w')
	f1 = open("d1_op.csv", 'w')
	f2 = open("d2_op.csv", 'w')
	f3 = open("d3_op.csv", 'w')
	f4 = open("d4_op.csv", 'w')
	positive_count = 0
	negative_count = 0
	for line in data:
		class_att = 4
		if ((line[4] == -1)):
			negative_count += 1
		else:
			positive_count += 1
		if ((negative_count < 1000 and line[class_att] == -1) or (positive_count < 1000 and line[class_att] == 1)):
			f0.write(str(line).strip('[,]') + "\n")
		elif ((negative_count < 2000 and line[class_att] == -1) or (positive_count < 2000 and line[class_att] == 1)):
			f1.write(str(line).strip('[,]') + "\n")
		elif ((negative_count < 3000 and line[class_att] == -1) or (positive_count < 3000 and line[class_att] == 1)):
			f2.write(str(line).strip('[,]') + "\n")
		elif ((negative_count < 4000 and line[class_att] == -1) or (positive_count < 4000 and line[class_att] == 1)):
			f3.write(str(line).strip('[,]') + "\n")
		elif ((negative_count < 5000 and line[class_att] == -1) or (positive_count < 5000 and line[class_att] == 1)):
			f4.write(str(line).strip('[,]') + "\n")


# Grab all of the attributes we want
def main():
	# create_files()
	# get_data()
	# normalize_data()
	process_op_data()

main()
