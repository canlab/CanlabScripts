#!/usr/bin/env python
#Note: This requires that pandas, numpy, and scipy are installed, and runs python 2.

#Usage: ./participant_screening-scebl_ot.py <CSV filename> <lines to take>

#<CSV filename> is the name of the CSV file you want to filter for suitability
#<lines to take> is an integer. The program will only look at the last <lines to take>
#lines of the CSV file. If left blank, it will look at the entire file.

import numpy as np
import scipy as sp
import pandas as pd
import sys, os

#This is the list of column headers to output.
column_out=["participant_info_complete","name1","email_address1","phone_number1","session_availability1","which_meds", 'i_was_bothered_by_things_t','i_did_not_feel_like_eating','i_felt_that_i_could_not_sh','i_felt_that_i_was_just_as','i_had_trouble_keeping_my_m','i_felt_depressed','i_felt_that_everything_i_d','i_felt_hopeful_about_the_f','i_thought_my_life_had_been','i_felt_fearful','my_sleep_was_restless','i_was_happy','i_talked_less_than_usual','i_felt_lonely','people_were_unfriendly','i_enjoyed_life','i_had_crying_spells','i_felt_sad','i_felt_that_people_dislike','i_could_not_get_going']

#This is the function that defines the relevant lines to
#print. It is a boolean function that takes one argument,
#the dataframe to filter.
def filter_function(df):
    return  (df['authorization___1'] == 1 and
             df['consent_to_contact1'] == 1 and
             df['painstudies'] == 1 and
             df['pain_screening1___6'] <= 1 and
             df['pain_screening1___7'] <= 1 and
             df['pain_screening1___12'] <= 1 and
             df['contact_heat'] == 0 and
             df['contact_cold'] == 0 and
             df['pain_sensitivity1'] == 0 and
             df['pain_amount1'] == 0 and
             (df['meds'] <= 1 or np.isnan(df['meds'])) and
             (df['pregnant1'] == 0 or np.isnan(df['pregnant1'])) and
             df['t'] <= 6 and
             df['a'] <= 6 and
             df['can'] <= 2 and
             df['co'] <= 3 and 
             df['am'] <= 3 and
             df['i'] <= 2 and
             df['s'] <=2 and
             df['h'] <= 3 and
             df['o'] <= 3 and
             df['other'] <= 2 and
             df['center_for_epidemiologic_studies_depression_scalec_complete'] == 2 and
             df['substance_use_history_complete'] == 2)




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

