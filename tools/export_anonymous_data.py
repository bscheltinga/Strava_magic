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
import time

    def Get_streams(ID):
        return streams


    def Save_xlsx(streams, title, folder):

    
    def Wait_API_limits():
        LimitFlag = 1
        print('Waiting for STRAVA API limits...')
        while LimitFlag == 1:
            time.sleep(15)  # Wait 15 seconds
            checktime = time.localtime()
            if checktime.tm_min % 15 == 0:
                print('Continuing syncing')
                LimitFlag = 0
        ApiLimitCounter = 0
        return ApiLimitCounter

# Set constants
ApiLimitCounter = 5

# List all activities
df = pd.read_excel('data/activities.xlsx')
df = df[df['manual']==False]

# Connect API - get access_token by running main.py
api = Client(access_token=access_token)

# Loop over activities
for ID in df['id']:
    print(ID)
    
    # Get streams
    
    # Save as xlsx
    
    # Increase API counter and check for limits
    ApiLimitCounter+=1
    if ApiLimitCounter > 495:
        ApiLimitCounter = Wait_API_limits()