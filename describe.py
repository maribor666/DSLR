import math
import argparse
import csv
import collections
from pprint import pprint


def_dataset_path = "./dataset_train.csv"

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset", help="Path to dataset for describing.", default=def_dataset_path)

	args = parser.parse_args()
	dataset_path = args.dataset

	file = open(dataset_path, mode='r')
	reader = csv.reader(file)
	lines = [line for line in reader]
	file.close()
	data = parse_data(lines)
	counts = [len(data[col_name]) for col_name in data if isinstance(data[col_name][0], float)]
	means = find_mean(data)
	stds = find_stds(data)
	minimals = [min(data[col_name]) for col_name in data if isinstance(data[col_name][0], float)]
	maximals = [max(data[col_name]) for col_name in data if isinstance(data[col_name][0], float)]
	quantiles25 = find_quantile(data, 0.25)
	quantiles50 = find_quantile(data, 0.5)
	quantiles75 = find_quantile(data, 0.75)
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
			if i == features_num:
				print('{:>15f}'.format(statistics[key][-1]), end='')
			else:
				for j in m:
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

	for col_name in data:
		data[col_name] = sorted(data[col_name])

	return data

if __name__ == '__main__':
	main()
