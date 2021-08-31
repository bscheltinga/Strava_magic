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
import os.path


def get_streams(ID):
    df_act = pd.DataFrame()  # Create the dataframe to store data

    # Define types of data and get streams
    types = ['time', 'distance', 'altitude', 'velocity_smooth',
             'heartrate', 'cadence', 'watts', 'temp', 'moving',
             'grade_smooth']
    streams = api.get_activity_streams(ID, types=types)
    keys = list(streams.keys())  # List available data
    for key in keys:
        df_act[key] = streams[key].data
    return df_act


def wait_API_limits():
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
datafolder = r"C:\Users\bscheltinga\Documents\Strava_magic\data\anonymized"

# List all activities
df = pd.read_excel('data/activities.xlsx')
df = df[df['manual']==False]
df = df.reset_index(drop=True)

# Connect API - get access_token by running main.py
api = Client(access_token=access_token)

# Loop over activities
for i, ID in enumerate(df['id']):
    print(ID)
    print(i)

    # Get streams
    df_act = get_streams(ID)

    # Increase API counter and check for limits
    ApiLimitCounter += 1
    if ApiLimitCounter > 595:
        ApiLimitCounter = wait_API_limits()

    # Save as xlsx
    name = df['start_date'][i]
    name = name.replace(" ", "_").replace("-", "_").replace(":", "")
    name = name + '.xlsx'
    folder_name = os.path.join(datafolder, name)
    df_act.to_excel(folder_name, index=False)
