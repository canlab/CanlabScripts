from redcap import Project
import os
import csv
import pandas

api_url = 'https://redcap.ucdenver.edu/api/'
api_key = os.environ['R_API_TOKEN']

project = Project(api_url, api_key)

csv_data = project.export_records(format='csv')

data_frame = project.export_records(format='df')

pandas.DataFrame.to_csv(data_frame,
"/work/ics/data/projects/wagerlab/labdata/data/Pain_Gen/Behavioral/raw/surveys/redcap/paingen_redcap.csv")
