import csv
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def_dataset_path = "./dataset_train.csv"

courses = [
	'Arithmancy',
	'Astronomy',
	'Herbology',
	'Defense Against the Dark Arts',
	'Divination',
	'Muggle Studies',
	'Ancient Runes',
	'History of Magic',
	'Transfiguration',
	'Potions',
	'Care of Magical Creatures',
	'Charms',
	'Flying'
]

houses = ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-dataset", help="Path to dataset for describing.", default=def_dataset_path)

	args = parser.parse_args()
	dataset_path = args.dataset

	try:
		df = pd.read_csv(dataset_path, index_col=0)
	except FileNotFoundError as e:
		print(e)
		exit(1)
	plt.figure(figsize=(8, 6))
	grouped_df = df.groupby('Hogwarts House')
	for course in courses:
		grouped_df[course].plot(kind='hist', alpha=0.5)
		plt.title(course)
		plt.show()

	print('Homogeneous are: Arithmancy, Care of Magical Creatures.')

if __name__ == '__main__':
	main()
