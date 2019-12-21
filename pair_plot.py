import pandas as pd
import matplotlib.pyplot as plt

dataset_path = "./dataset_train.csv"

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
	try:
		df = pd.read_csv(dataset_path, index_col=0)
	except FileNotFoundError as e:
		print(e)
		exit()

	grouped_df = df.groupby('Hogwarts House')

	fig, axes = plt.subplots(13, 13, figsize=(15, 10))
	fig.subplots_adjust(hspace=0.1, wspace=0.1)
	for ax in axes:
		for a in ax:
			a.set_xticklabels([])
			a.set_yticklabels([])
			a.tick_params(axis='both', width=0)

	for i in range(len(courses)):
		grouped_df[courses[i]].plot(kind='hist', alpha=0.5, ax=axes[i][i])
		axes[i][i].set_xlabel(courses[i].replace(' ', '\n'), fontsize=8)
		axes[i][i].set_ylabel(courses[i].replace(' ', '\n'), fontsize=8)


	for i, xi in enumerate(courses):
		for j, yi in enumerate(courses):
			if j < i:
				axes[i][j].remove()
				continue
			if xi == yi:
				continue
			ravenclowX = grouped_df.get_group('Ravenclaw')[xi]
			slytherinX = grouped_df.get_group('Slytherin')[xi]
			gryffindorX = grouped_df.get_group('Gryffindor')[xi]
			hufflepuffX = grouped_df.get_group('Hufflepuff')[xi]


			ravenclowY = grouped_df.get_group('Ravenclaw')[yi]
			slytherinY = grouped_df.get_group('Slytherin')[yi]
			gryffindorY = grouped_df.get_group('Gryffindor')[yi]
			hufflepuffY = grouped_df.get_group('Hufflepuff')[yi]

			axes[i][j].plot(ravenclowX, ravenclowY, 'v', markersize=.5, color='blue')
			axes[i][j].plot(slytherinX, slytherinY, '^', markersize=.5, color='green')
			axes[i][j].plot(gryffindorX, gryffindorY, 'o', markersize=.5, color='red')
			axes[i][j].plot(hufflepuffX, hufflepuffY, 's', markersize=.5, color='yellow')
	plt.show()

if __name__ == "__main__":
	main()