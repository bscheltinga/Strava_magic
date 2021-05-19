# -*- coding: utf-8 -*-
"""
Create a 0/1 array from the injury input data from the excel file

@author: bscheltinga
"""
import pandas as pd
from datetime import date
import os.path
import numpy as np


# Create data frame with all dates
start = date(2013, 2, 13)
end = date.today()
delta = end-start

rng = pd.date_range(start=start, periods=delta.days, freq='D')
df_injury = pd.DataFrame({ 'Date': rng})

# Read injury file
path = os.getcwd()
path = path.strip('tools')
path = path + 'data\BlessuresNa2016.xlsx'
df = pd.read_excel (path)

for i in range(0,len(df)):
    datelist = pd.date_range(df.Datum[i], periods=df.Days[i]).tolist()
    injurysite = df.Blessure[i]*df.Days[i]





df = df.append({'Datum': pd.Timestamp.today()},ignore_index=True)
df.set_index('Datum', inplace=True)
df = df.resample('D').last()
df = df.drop(columns=['Notitie'])


