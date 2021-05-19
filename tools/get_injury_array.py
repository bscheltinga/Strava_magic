# -*- coding: utf-8 -*-
"""
Create a 0/1 array from the injury input data from the excel file

@author: bscheltinga
"""
import pandas as pd
from datetime import timedelta, date
import os.path
import numpy as np


# Create data frame with all dates
start = date(2013, 2, 13)
end = date(2021, 4, 11)
delta = end-start

rng = pd.date_range(start=start, periods=delta.days, freq='D')
df_injury = pd.DataFrame({ 'Date': rng})
df_injury.set_index('Date', inplace=True)
df_injury['Injured'] = np.zeros(len(df_injury))
df_injury['Injury_site'] = ['None']*len(df_injury)

# Read injury file
path = os.getcwd()
path = path.strip('tools')
path = path + '\data\BlessuresNa2016.xlsx'
df = pd.read_excel (path)


for i in range(0,len(df)):
    start = df.Datum[i] 
    
    rng = pd.date_range(start=start, periods=df.Days[i], freq='D')
    df_this_injury = pd.DataFrame({ 'Date': rng})
    df_this_injury.set_index('Date', inplace=True)
    
    for j in df_this_injury.index:
        print(j)
        df_injury['Injured'][j] = 1
        df_injury['Injury_site'][j] = df['Blessure'][i]
        
        
# Save it to a excel
df_injury.to_excel(r'data/Data_science_injuries.xlsx')
