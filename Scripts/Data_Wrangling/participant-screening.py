#!/usr/bin/env python
#Note: This requires that pandas, numpy, and scipy are installed, and runs python 2.

#Usage: ./participant_screening.py <CSV filename> <lines to take>

#<CSV filename> is the name of the CSV file you want to filter for suitability
#<lines to take> is an integer. The program will only look at the last <lines to take>
#lines of the CSV file. If left blank, it will look at the entire file.

import numpy as np
import scipy as sp
import pandas as pd
import sys, os

#This is the list of column headers to output.
column_out=["participant_info_complete","name1","email_address1","phone_number1","session_availability1","which_meds"]

#This is the function that defines the relevant lines to
#print. It is a boolean function that takes one argument,
#the dataframe to filter.
def filter_function(df):
    return  (df['consent1'] == 1 and
             df['authorization___1'] == 1 and
             df['consent_to_contact1'] == 1 and
             df['painstudies'] == 1 and
             df['pain_screening1___6'] <= 1 and
             df['pain_screening1___7'] <= 1 and
             df['pain_screening1___13'] <= 1 and
             df['contact_heat'] == 0 and
             df['contact_cold'] == 0 and
             df['pain_sensitivity1'] == 0 and
             df['pain_amount1'] == 0 and
             (df['meds'] <= 1 or np.isnan(df['meds'])) and
             df['fmri_studies_consent'] == 1 and
             df['study_screening1___6'] == 1 and
             df['mri_screening1___16'] <= 1 and
             df['mri_screening1___19'] <= 1 and
             (df['welder_machinist'] == 0 or np.isnan(df['metal_eyes1'])) and
             (df['metal_eyes1'] == 0 or np.isnan(df['metal_eyes1'])) and
             (df['pregnant1'] == 0 or np.isnan(df['pregnant1'])) and
             df['contact_lenses1'] != 1)

relevant_items=['consent1','authorization___1','consent_to_contact1','painstudies','pain_screening1___6','pain_screening1___7','pain_screening1___13','do_you_have_chronic_low_ba','contact_heat','contact_cold','pain_sensitivity1','pain_amount1','meds','fmri_studies_consent','study_screening1___6','mri_screening1___16','mri_screening1___19','welder_machinist','metal_eyes1','pregnant1','contact_lenses1','contact_lenses1']

filename=sys.argv[1]
endlines=True
try:
    last_lines=int(sys.argv[2])+1
except (IndexError):
    endlines=False
    last_lines=0
screening_dataframe=pd.read_csv(filename)
if endlines:
    screening_dataframe=screening_dataframe[-last_lines:]
filtered_dataframe=screening_dataframe[screening_dataframe.apply(filter_function, axis=1)]
output_dataframe=filtered_dataframe[column_out]

print output_dataframe.to_csv(index=False)

