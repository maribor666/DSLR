import json
import argparse
import sys
import os
import csv
import pandas as pd
import numpy as np


DATA_FILE = "data.json"
PREDICTION_FILE = "houses.csv"
HOUSES_COL = "Hogwarts House"
SELECTED_FEATURES = ["Herbology", "Ancient Runes", "Astronomy", "Charms", "Defense Against the Dark Arts"]
T0_LABEL = "t0"


class LogRegPredict:
    def __init__(self, data_json):
        self.theta_dic = data_json['houses']
        self.std_devs = data_json['standard']['std']
        self.means = data_json['standard']['mean']

    def prediction(self, thetas, data):
        house = None
        score = None
        for key, value in thetas.items():
            tmp = np.dot(thetas[key], data)
            if (score is None or tmp > score):
                score = tmp
                house = key
        return house

    def standardize(self, matrix):
        return (matrix - self.means) / self.std_devs

    def save_prediction_as_csv(self, predictions):
        with open(PREDICTION_FILE, 'w+') as fd:
            writer = csv.writer(fd)
            writer.writerow(['Index', HOUSES_COL])
            for each in predictions:
                writer.writerow([each[0], each[1]])

    def predict(self, df):
        df.loc[:, SELECTED_FEATURES] = self.standardize(df.loc[: , SELECTED_FEATURES])
        df = df.loc[:, SELECTED_FEATURES]
        df.insert(1, T0_LABEL, np.ones(df.shape[0]))
        df = df.dropna()
        predictions = []
        for index, row in df.iterrows():
            predictions.append((index, self.prediction(self.theta_dic, row)))
        self.save_prediction_as_csv(predictions)



if __name__ == '__main__':
    args = argparse.ArgumentParser("Predict houses from dataset")
    args.add_argument("file", help="Dataset without nececcary information that we need to find through prediction", type=str)
    args = args.parse_args()
    if os.path.isfile(args.file):
        try:
            df = pd.read_csv(args.file, sep=',')
            json_file = open(DATA_FILE)
            data_json = json.load(json_file)
            log_reg_predict = LogRegPredict(data_json)
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
            sys.exit(1)
    else:
        sys.stderr.write("Errors occured while opening file\n")
        sys.exit(1)
    log_reg_predict.predict(df)
