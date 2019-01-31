#!/usr/bin/envpython3
# coding: utf-8

import os
import csv
import re
import math
import pandas as pd
from datetime import datetime
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem import RSLPStemmer
from operator import itemgetter
from collections import Counter
from preprocess import Preprocess
from analyser import Analyser
from itertools import groupby
from sklearn import preprocessing


class Process(object):
    """docstring for Process."""
    def __init__(self, filename):
        super(Process, self).__init__()
        self.file = filename

    def check_preprocess(self):
        return True if os.path.isfile('preprocessed.csv') else False

    def calculate_date(self, date):
        if date == 'Date': return None
        date_format = "%d-%m-%Y"
        today = datetime.now()
        someday = datetime.strptime(date, date_format)
        diff = today - someday
        return diff.days

    def decay_date(self, value):
        return math.exp(-value/25)

    def confiability_score(self, votes_up, votes_down, n_tips):
        if votes_up != 0:
            votes_up = math.log2(votes_up)
        if votes_down != 0:
            votes_down = 2 ** votes_down
            #votes_down = math.exp(-votes_down)

        n_tips = math.log1p(n_tips)

        return votes_up + votes_down + n_tips

    def method(self):
        if not self.check_preprocess():
            p = Preprocess(self.file)
            p.preprocess()
            print('File preprocessed!')
        else:
            print('Already preprocessed file.')

        with open('preprocessed.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            data = []
            data_df = []
            for row in reader:
                value = self.calculate_date(row[7])
                if value:
                    data.append((row[0],self.decay_date(value)))

            for key, group in groupby(data, key=lambda x: x[0]):
                data_df.append([key, sum(j for i, j in group)])

            df = pd.DataFrame(data_df, columns=['establishment','decay_date'])

        # Create x, where x the 'final_metric' column's values as floats
        x = df[['decay_date']].values.astype(float)

        # Create a minimum and maximum processor object
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(1,10))

        # Create an object to transform the data to fit minmax processor
        x_scaled = min_max_scaler.fit_transform(x)

        # Run the normalizer on the dataframe
        df_normalized = pd.DataFrame(x_scaled)

        df.drop('decay_date', axis=1, inplace=True)
        df_normalized = df_normalized.rename(columns={0:'decay_date'})
        df = pd.concat([df, df_normalized],axis=1)

        a = Analyser(df)
        #a.polarity()
        #a.confiability()
        a.viewer('pol','conf')
        df = a.mname()
        return df
