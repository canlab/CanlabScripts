#!/usr/bin/env python
#Note: This requires that pandas, numpy, and scipy are installed, and runs python 3.

#Usage: ./participant_screening.py <CSV filename> <lines to take>

#<CSV filename> is the name of the CSV file you want to filter for suitability
#<lines to take> is an integer. The program will only look at the last <lines to take>
#lines of the CSV file. If left blank, it will look at the entire file.

import numpy as np
import scipy as sp
import pandas as pd
import sys, os

#This is the list of column headers to output.
column_out=["participant_form_timestamp","participant_info_complete","name1","sex1","email_address1","phone_number1","session_availability1","which_meds", "flags"]

#This is the function that defines the relevant lines to
#print. It is a boolean function that takes one argument,
#the dataframe to filter.
#filter_function filters out participants that do not meet
#basic pain study requirements/consent
def filter_function(df):
    return  (df['consent_to_contact1'] == 1 and
             df['authorization___1'] == 1 and
             df['dominant_hand'] != 2 and
             df['painstudies'] == 1 and
             df['pain_screening1___8'] != 1 and
             df['pain_screening1___9'] != 1 and
             df['do_you_have_chronic_pain'] == 0 and
             df['contact_heat'] == 0 and
             df['contact_cold'] == 0 and
             df['pain_sensitivity1'] == 0 and
             df['pain_amount1'] == 0 and
             (df['meds'] <= 1 or np.isnan(df['meds'])) and
             df['fmri_studies_consent'] == 1 and
             df['study_screening1___6'] == 1 and
             (df['welder_machinist'] == 0 or np.isnan(df['metal_eyes1'])) and
             (df['metal_eyes1'] == 0 or np.isnan(df['metal_eyes1'])) and
             (df['pregnant1'] == 0 or np.isnan(df['pregnant1'])))

#combine_flags fuction screens participants for MRI safety concerns
#Will populate 'flags' column in final .csv with MRI contradictions
#Subject recruiter should discuss MRI flags before scheduling
def combine_flags(df):
    filtered_dataframe = df
    filtered_dataframe['flags'] = ''
    for index, row in filtered_dataframe.iterrows():
        if row['mri_screening1___1'] == 1:
            filtered_dataframe.loc[index, 'flags'] = filtered_dataframe.loc[index, 'flags'] + "Aneurysm clips; "
        if row['mri_screening1___2'] == 1:
            filtered_dataframe.loc[index, 'flags'] = filtered_dataframe.loc[index, 'flags'] + "Intracranial bypass graft clips; "
        if row['mri_screening1___3'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Coronary artery bypass clips or cardiac valve; '
        if row['mri_screening1___4'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Renal transplant clips; '
        if row['mri_screening1___5'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Other vascular clips or filters; '
        if row['mri_screening1___6'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Surgical staples or wire sutures; '
        if row['mri_screening1___7'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Cardiac pacemaker or pacemaker wires; '
        if row['mri_screening1___8'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Middle ear or orbital eye prothesis; '
        if row['mri_screening1___9'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Artificial joint or limb prosthesis; '
        if row['mri_screening1___10'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Surgical screws, nails or rods; '
        if row['mri_screening1___11'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Breast tissue expander; '
        if row['mri_screening1___12'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Neurostimulator; '
        if row['mri_screening1___13'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Biostimulator; '
        if row['mri_screening1___14'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Shrapnel/bullets; '
        if row['mri_screening1___15'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Hearing aids; '
        if row['mri_screening1___16'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'IUD; '
        if row['mri_screening1___17'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'Magnetic dental appliances or fillings; '
        if row['mri_screening1___18'] == 1:
            filtered_dataframe.loc[index, 'flags'] =  filtered_dataframe.loc[index, 'flags'] + 'ONE OR MORE MRI SAFETY CONCERNS; '
        if row['contact_lenses1'] != 3:
            filtered_dataframe.loc[index, 'flags'] = filtered_dataframe.loc[index, 'flags'] + 'glasses; '
        if filtered_dataframe.loc[index, 'flags'] == '':
            filtered_dataframe.loc[index, 'flags'] = 'No Flags'
    return filtered_dataframe


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
df_to_print = combine_flags(filtered_dataframe)
output_dataframe=df_to_print[column_out]

print (output_dataframe.to_csv(index=False))
