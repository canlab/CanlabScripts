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
#remove worthless columns
rd.drop(rd.columns[[0,1,2,48]], axis=1, inplace=True)

#filtering for all exclusions
rd_filtered = rd[
    (rd.age_in_range == 1) &
    (((rd.backpain_length > 1) & (rd.backpain_frequency > 1) & (rd.backpain_intensity > 3)) |
    ((rd.backpain_length == 0) & (rd.backpain_frequency == 1) & (rd.backpain_intensity == 0))) &
    (rd.current_opioid_use == 2) &
    (rd.pregnancy == 2) &
    (rd.english_proficiency == 1) &
    (rd.transportation == 1) &
    (rd.sick == 2) &
    (rd.immunosuppressant == 2) &
    (rd.autoimmune == 2) &
    (rd.have_you_ever_been_diagnos == 2) &
    (rd.have_you_ever_been_diagnos2 == 2) &
    (rd.in_the_past_year_have_you == 2) &
    (rd.do_you_have_difficulty_con == 2) &
    (rd.stroke_neurological_event == 2) &
    (rd.do_you_use_intravenous_dru == 2) &
    (rd.welder == 2) &
    (rd.metaleye == 2) &
    (rd.metalbody == 2) &
    (rd.claustrophobic == 2) &
    (rd.mri_safety == "20")
]

#remove worthless columns
rd_filtered.drop(rd_filtered.columns[[0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,35,36,38,39,40,41,42,43]], axis=1, inplace=True)

#assign patient/control labels

#filter for patient/control specifics

#print results to new csv sheet
#name
#patient/control
#gender
#age
#email
#phone
rd_filtered.to_csv('~/Documents/WAVi/rdprocessed.csv')
print(rd_filtered)
