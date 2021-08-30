# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 16:16:57 2021

This script will use the dataframe with all data and export each non-manual
acitivity as .xlsx in the folder data/anonymous_data. The files contain
all original data except for GPS-data. Sampling rate is the original rate.

@author: bscheltinga
"""

import pandas as pd
from stravalib import Client

def Get_streams(ID):
    return streams

def Save_xlsx(streams, title, folder):

# List all activities
df = pd.read_excel('data/activities.xlsx')
df = df[df['manual']==False]

# Connect API - get access_token by running main.py
api = Client(access_token=access_token)

# Loop over activities
for ID in df['id']:
    print(ID)
    
# Get streams

# Export as .xlsx