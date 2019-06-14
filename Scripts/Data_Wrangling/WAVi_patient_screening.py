#!/usr/bin/env python3

#usage: ./WAVi_patient_screening.py <CSV filename>

import numpy as np
import scipy as sp
import pandas as pd
import sys, os

#read first argument into pandas df from CSV file, set row index to 0 (REDCAP id)
redcap_data = pd.read_csv(sys.argv[1], index_col = 0)

#set list of column names from df
column_list = redcap_data.columns.values.tolist()

#cleaning
#print(redcap_data.iloc[:1,0:2])
#print(redcap_data.iloc[:,1])
redcap_data.drop(['redcap_event_name','redcap_survey_identifier','eligibility_prescreening_timestamp'], axis=1)

print(redcap_data)
#remove bad rows
#can't use complete, unresolved

#create exclusion flags

#filter for MRI
#assign patient/control labels

#filter for exclusion
#patient
#control

#print results
#name
#patient/control
#gender
#age
#email
#phone
#print(redcap_data)
