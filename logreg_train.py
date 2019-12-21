import sys
import math
import csv
import os
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TEST_DATASET="./ressources/dataset_test.csv"
# TRAIN_DATASET="./ressources/dataset_train.csv"
DATA_FILE = "data.json"
HOUSES_COL = "Hogwarts House"
SELECTED_FEATURES = ["Herbology", "Ancient Runes", "Astronomy", "Charms", "Defense Against the Dark Arts"]
T0_LABEL = "t0"


class LogRegTrain:
    def __init__(self, data, iterations, learn_rate, visu):
        data.insert(0, T0_LABEL, np.ones(data.shape[0]))
        self.selected_features = [HOUSES_COL] + [T0_LABEL] + SELECTED_FEATURES
        self.data = data.loc[:, self.selected_features]
        self.data = self.data.dropna()
        self.learn_rate = learn_rate
        self.visu = visu
        self.iterations = iterations
        self.predictions = {}
        self.houses = self.data.loc[:, HOUSES_COL]
        self.houses_set = self.data.loc[:, HOUSES_COL].unique()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def is_from_house(self, house):
        return np.where(self.houses == house, 1, 0)

    def standardize(self, matrix):
        return [matrix.std(), matrix.mean(), ((matrix - matrix.mean()) / matrix.std())]

    def gradient(self, m, y, h):
        return (1 / m) * (np.dot(-y.T, np.log(h)) - np.dot((1 - y).T, np.log(1 - h)))
    
    def save_result_in_json(self):
        with open(DATA_FILE, 'w+') as json_file:  
            json.dump(self.predictions,  json_file)

    def train(self):
        std_deviations, means, x = self.standardize(self.data.loc[:, self.selected_features[2:]])
        x.insert(0, T0_LABEL, self.data.loc[:, T0_LABEL])
        self.predictions['standard'] = {'std': list(std_deviations), 'mean': list(means)}
        self.predictions['houses'] = {}
        m = x.shape[0]
        for house in self.houses_set:
            cost = []
            thetas = np.zeros((x.shape[1]))
            y = self.is_from_house(house)
            for i in range(self.iterations):
                z = np.dot(x, thetas)
                h = self.sigmoid(z)
                j = self.gradient(m,y,h)
                cost.append(j)
                gradient = np.dot(x.T, (h - y)) / y.size
                thetas -= self.learn_rate * gradient
            self.predictions['houses'][house] = list(thetas)
            if self.visu:
                plt.plot(cost ,label=house)
        if self.visu:
            plt.legend()
            plt.show()
        self.save_result_in_json()

    

if __name__ == '__main__':
    args = argparse.ArgumentParser("Statistical description of dataset")
    args.add_argument("file", help="Dataset in format csv", type=str)
    args.add_argument("-i", "--iter", help="Iterations count to go through the regression", default=10000, type=int)
    args.add_argument("-l", "--learning", help="Learning rate for regression", default=0.01, type=float)
    args.add_argument("-v", "--visu", help="Visualize cost evolution", default=False, action="store_true")
    args = args.parse_args()

    if os.path.isfile(args.file):
        try:
            df = pd.read_csv(args.file, sep=',')
            LogRegTrain(df, args.iter, args.learning, args.visu).train()
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
            sys.exit(1)
    else:
        sys.stderr.write("Invalid input\n")
        sys.exit(1)
