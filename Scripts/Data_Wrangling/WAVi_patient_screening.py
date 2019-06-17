#!/usr/bin/env python3

#ENVIRONMENT

#usage: ./WAVi_patient_screening.py <CSV filename>

import numpy as np
import scipy as sp
import pandas as pd
import sys, os

#read first argument into pandas df from CSV file, set row index to 0 (REDCAP id)
rd = pd.read_csv(sys.argv[1], index_col = 0)

#set list of column names from df
column_list = rd.columns.values.tolist()

#CLEANING
#remove bad rows
rd.drop(rd.columns[[0,1,2,48]], axis=1, inplace=True)

#exclude for age
rd_filtered = rd.query(
'age_in_range==1'
)

#create exclusion flags

#filter for MRI
#assign patient/control labels

#filter for exclusion
#patient
#control

#print results to new csv sheet
#name
#patient/control
#gender
#age
#email
#phone
rd_filtered.to_csv('~/Documents/WAVi/rdprocessed.csv')
print(rd)
