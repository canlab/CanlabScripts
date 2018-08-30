#!/usr/bin/env python
#Note: This requires that pandas, numpy, and scipy are installed, and runs python 3.

#Usage: ./participant_screening.py <CSV filename> <lines to take>

#<CSV filename> is the name of the CSV file you want to filter for suitability
#<lines to take> is an integer. The program will only look at the last <lines to take>
#lines of the CSV file. If left blank, it will look at the entire file.

import numpy as np
import scipy as sp
import pandas as pd
import sys, os, re
import datetime as dt
from math import floor


#This is the list of column headers to output.
column_out=["participant_info_complete","name1","email_address1","phone_number1","date_of_birth1","sex1", "comments1"]

# Get approximate age from date of birth. This is imprecise and fudges leap days,
# but should never be more than a few days off.

def age_from_date(strdob):
    try:
        dateparts=re.split('[/-]', strdob)
        dateparts=[int(x) for x in dateparts]
        dob=dt.date(year=dateparts[2]+1900, month=dateparts[0], day=dateparts[1]) # Date object
        age=dob.today()-dob
        return floor(age.days/365.25)
    except(ValueError):
    	print 'error with age calculation for ' + strdob
        print dateparts
        raise ValueError

#This is the function that defines the relevant lines to
#print. It is a boolean function that takes one argument,
#the dataframe to filter.

def filter_function(df):
    age = df['date_of_birth1']
    strdob=df['date_of_birth1']
    age=age_from_date(strdob)
    youngerThan70=age <= 70 # Younger than 70
    olderThan21=age >= 21  # Older than 38
    ageOK=youngerThan70 and olderThan21
    return  (
            #ageOK and
            df['authorization___1'] == 1 and
            df['painstudies'] == 1 and
            df['do_you_have_chronic_pain'] == 1 and
            df['do_you_have_chronic_low_ba'] == 1 and
            df['fmri_studies_consent'] == 1 and
            df['study_screening1___3'] == 0 and
            df['study_screening1___4'] == 0 and
            (df['welder_machinist'] == 0 or np.isnan(df['welder_machinist'])) and
            (df['metal_eyes1'] == 0 or np.isnan(df['metal_eyes1'])) and
            (df['pregnant1'] == 0 or np.isnan(df['pregnant1'])))

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
filtered_dataframe['date_of_birth1']=filtered_dataframe['date_of_birth1'].apply(age_from_date)
output_dataframe=filtered_dataframe[column_out]

print (output_dataframe.to_csv(index=False))
print
print
print('REMEMBER: CHECK EVERYONES metal in body, study screening form, and contact lens IN THE REDCAP!')
print ' THIS IS NOT SCREENED FOR BY THIS SCRIPT'
