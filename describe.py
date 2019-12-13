import math
import argparse # add argparse
import csv
import collections
from pprint import pprint


dataset_path = "./dataset_train.csv"

def main():
	file = open(dataset_path, mode='r')
	reader = csv.reader(file)
	lines = [line for line in reader]
	file.close()
	data = parse_data(lines)
	# for col_name in data:
		# print(col_name, data[col_name][0])
	# ill count numerical features only where column names is number except 'Index'
	counts = [len(data[col_name]) for col_name in data if isinstance(data[col_name][0], float)]
	# pprint(counts)
	means = find_mean(data)
	# pprint(means)
	stds = find_stds(data)
	# pprint(stds)
	minimals = [min(data[col_name]) for col_name in data if isinstance(data[col_name][0], float)]
	# pprint(minimals)
	maximals = [max(data[col_name]) for col_name in data if isinstance(data[col_name][0], float)]
	# pprint(maximals)
	quantiles25 = find_quantile(data, 0.25)
	# pprint(quantiles25)
	quantiles50 = find_quantile(data, 0.5)
	# pprint(quantiles50)
	quantiles75 = find_quantile(data, 0.75)
	# pprint(quantiles75)
	statistics = {
		'Count': counts,
		'Mean': means,
		'Std': stds,
		'Min': minimals,
		'25%': quantiles25,
		'50%': quantiles50,
		'75%': quantiles75,
		'Max': maximals
	}
	print_output(statistics)
	
def print_output(statistics):
	features_num = len(statistics['Count'])
	i = 0
	m = [1, 2, 3, 4][::-1]
	while i < features_num:
		k = 0
		print("               ", end="")
		while k < 4:
			s = 'Feature ' + str(i + 1)
			s = '{0:>15}'.format(s)
			print(s, end='')
			k += 1
			i += 1
			if i == features_num:
				break
		print()
		for key in statistics:
			print("{:15}".format(key), end='')
			# print(i,'|', end='')
			if i == features_num:
				print('{:>15f}'.format(statistics[key][-1]), end='')
			else:
				for j in m:
					# print(j, end='')
					print('{:>15f}'.format(statistics[key][i - j]), end='')

			print()



def find_quantile(data, q):
	quantiles = []
	for col_name in data:
		if not isinstance(data[col_name][0], float):
			continue
		quantile = data[col_name][round(len(data[col_name]) * q)]
		quantiles.append(quantile)
	return quantiles


def find_stds(data):
	stds = []
	for col_name in data:
		if not isinstance(data[col_name][0], float):
			continue
		summa = 0
		mean = sum(data[col_name]) / len(data[col_name])
		for el in data[col_name]:
			summa += (el - mean) ** 2
		std = math.sqrt(summa / len(data[col_name]))
		stds.append(std)
	return stds

def find_mean(data):
	means = []
	for col_name in data:
		if not isinstance(data[col_name][0], float):
			continue
		mean = sum(data[col_name]) / len(data[col_name])
		means.append(mean)
	return means


def parse_data(lines):
	data = collections.OrderedDict()
	for el in lines[0]:
		data[el] = []
	for line in lines[1:]:
		for el, col_name in zip(line, data):
			if col_name == 'Index':
				data[col_name].append(int(el))
			if el == '':
				continue
			if el == 'Nan' or el == 'nan':
				data[col_name].append(el)
				continue
			try:
				val = float(el)
			except ValueError:
				data[col_name].append(el)
				continue
			data[col_name].append(val)
	
	# for col_name in data:
	# 	types = set([type(el) for el in data[col_name]])
	# 	print(types)

	for col_name in data:
		data[col_name] = sorted(data[col_name])

	return data

if __name__ == '__main__':
	main()
