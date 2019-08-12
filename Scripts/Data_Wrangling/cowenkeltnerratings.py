#!/usr/bin/env python3

# Usage: ./cowenkeltnerratings.py <filename>

import pandas as pd
import numpy as np
import os, sys

# import csv using pandas
ratings = pd.read_csv(sys.argv[1], index_col = 0)

# create array of labels
labels = ratings.columns.values
print(labels)

# test = ratings.sort_values('Triumph')["Filename"].head(10)
# print(test)

allTopTen = pd.DataFrame(columns = ratings.columns.values)

for emotion in labels:
    topTen = ratings.sort_values(emotion, ascending=False)[:10][emotion].index.values
    allTopTen[emotion] = topTen

allTopTen.to_csv('~/Downloads/TopTenRatings.csv')
