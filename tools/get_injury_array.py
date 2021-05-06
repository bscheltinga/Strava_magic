# -*- coding: utf-8 -*-
"""
Create a 0/1 array from the injury input data from the excel file

@author: bscheltinga
"""
import pandas as pd
from datetime import date
import os.path


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