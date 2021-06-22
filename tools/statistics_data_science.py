# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:19:40 2021

@author: bscheltinga

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from tabulate import tabulate

# Load data
df_non_injur = pd.read_excel(r'C:\Users\bscheltinga\OneDrive - Universiteit Twente\Data Science\Project\Tabellen\Selected_injuries.xlsx')
df_injur = pd.read_excel(r'C:\Users\bscheltinga\OneDrive - Universiteit Twente\Data Science\Project\Tabellen\Selected_non_injuries.xlsx')

# Calculate means

workloads = ['moving_time','dis_speed_high','dis_speed_low']
models = ['AL', 'ACWR', 'trainingspeaks']
param_list = []
mean_injur = []
mean_non_injur = []
t_stats = []
p_vals = []
for mdl in models:
    for wrk in workloads:   
        param = mdl+'_'+ wrk
        param_list.append(param)
        
        mean_injur.append(np.mean(df_injur[param]))
        mean_non_injur.append(np.mean(df_non_injur[param]))
        
        # Paired sample ttest
        
        [t_stat ,p_val] = stats.ttest_rel(df_injur[param], df_non_injur[param])
        t_stats.append(t_stat)
        p_vals.append(p_val)
        
        plt.figure();
        plt.hist(df_non_injur[param],bins=25, label='Non Injured')
        plt.hist(df_injur[param],bins=25, label='Inured')
        plt.legend()
        plt.title('Histograms ' + param)
                 
        
# Make dataframe
df = pd.DataFrame()
df['Model'] = param_list
df['Mean non-injured'] = mean_non_injur
df['Mean injured'] = mean_injur
df['t-stats'] = t_stats
df['p-value'] = p_vals

# df.to_excel(r'C:\Users\bscheltinga\OneDrive - Universiteit Twente\Data Science\Project\Tabellen\statistics.xlsx')
