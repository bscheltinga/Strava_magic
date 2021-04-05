# Implementation of fitness fatigue model
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
Using df_acts workload parameters as input data.

'''

def create_ff_df(df_acts):
    '''
    Set the workload parameters from df_acts in ff_df.
    Set 0 it no activity was done.
    '''
    columns = ['banister_trimp','dis_speed_high','dis_speed_low','distance',
               'edwards_trimp','moving_time','lucia_trimp','lucia_trimp_speed',
               'trimp_norm_distance','trimp_norm_hr']
    ff_df = df_acts.resample('D', on='start_date')[columns].sum()

    return ff_df

def ff_model(ff_df,params, model='trainingspeaks'):
    '''
    Suported models: banister, trainingspeaks, calvert (not finished), ACWR
    '''
    ff_df['fitness'] = np.zeros(len(ff_df))
    ff_df['fatigue'] = np.zeros(len(ff_df))
    ff_df['form'] = np.zeros(len(ff_df))
        
    if model == 'trainingspeaks':
        # Model equations according to trainingpeaks/elevate    
        for i in range(len(ff_df)):
            if i == 0:
                ff_df['fitness'][0] = 0 + (ff_df['b_trimp'][0] - 0)*(1-np.exp(-1/params[0]))
                ff_df['fatigue'][0] = 0 + (ff_df['b_trimp'][0] - 0)*(1-np.exp(-1/params[1]))
                ff_df['form'][0] = 0
            else:
                ff_df['fitness'][i] = ff_df['fitness'][i-1] + (ff_df['b_trimp'][i] - ff_df['fitness'][i-1])*(1-np.exp(-1/params[0]))
                ff_df['fatigue'][i] = ff_df['fatigue'][i-1] + (ff_df['b_trimp'][i] - ff_df['fatigue'][i-1])*(1-np.exp(-1/params[1]))
                ff_df['form'][i] = ff_df['fitness'][i-1] - ff_df['fatigue'][i-1]
            
    if model == 'banister':
#     Model equations according to equation 10/11 from
    # B. S. Hemingway, L. Greig, and P. Swinton, “A NARRATIVE REVIEW OF MATHEMATICAL FITNESS-FATIGUE MODELLING FOR APPLICATIONS IN EXERCISE SCIENCE: MODEL DYNAMICS, METHODS, LIMITATIONS, AND FUTURE RECOMMENDATIONS A,” 2020, doi: 10.31236/osf.io/ap75j.
    # fitness/fatigue = Value yesterday*exp(param) + workload
        for i in range(len(ff_df)):
            if i == 0:
                ff_df['fitness'][0] = 0 + (ff_df['b_trimp'][0])
                ff_df['fatigue'][0] = 0 + (ff_df['b_trimp'][0])
                ff_df['form'][0] = 0
            else:
                ff_df['fitness'][i] = ff_df['fitness'][i-1]*(np.exp(-1/params[0])) + ff_df['b_trimp'][i]
                ff_df['fatigue'][i] = ff_df['fatigue'][i-1]*(np.exp(-1/params[1])) + ff_df['b_trimp'][i]
                ff_df['form'][i] = ff_df['fitness'][i-1] - ff_df['fatigue'][i-1]
                
    if model == 'calvert':
#     Model equations according to equation 12 from
    # B. S. Hemingway, L. Greig, and P. Swinton, “A NARRATIVE REVIEW OF MATHEMATICAL FITNESS-FATIGUE MODELLING FOR APPLICATIONS IN EXERCISE SCIENCE: MODEL DYNAMICS, METHODS, LIMITATIONS, AND FUTURE RECOMMENDATIONS A,” 2020, doi: 10.31236/osf.io/ap75j.
    # fitness/fatigue = Value yesterday*exp(param) + workload (+ extra delay for fitness)
        for i in range(len(ff_df)):
            if i == 0:
                ff_df['fitness'][0] = 0 + (ff_df['b_trimp'][0])
                ff_df['fatigue'][0] = 0 + (ff_df['b_trimp'][0])
                ff_df['form'][0] = 0
            else:
                ff_df['fitness'][i] = ff_df['fitness'][i-1]*(np.exp(-1/params[0]) - np.exp(-1/3)) + ff_df['b_trimp'][i]
                ff_df['fatigue'][i] = ff_df['fatigue'][i-1]*(np.exp(-1/params[1])) + ff_df['b_trimp'][i]
                ff_df['form'][i] = ff_df['fitness'][i-1] - ff_df['fatigue'][i-1]
                
    if model == 'ACWR':
#     Model equations according to acute/chronic workload. Note that we not speak of fatigue and fintess but acute
        # and chronic workload. The fitness: chronic, fatigue: acute and form (acute/chronic)
        # it uses a rectangular window for the summation.
        for i in range(len(ff_df)):
            if i <= params[0] and i <= params[1]:
                ff_df['fitness'][i] = sum(ff_df['b_trimp'][0:i])
                ff_df['fatigue'][i] = sum(ff_df['b_trimp'][0:i])
            elif i <= params[0] and i > params[1]:
                ff_df['fitness'][i] = sum(ff_df['b_trimp'][0:i])
                ff_df['fatigue'][i] = sum(ff_df['b_trimp'][i-params[1]:i])
            else:
                ff_df['fitness'][i] = sum(ff_df['b_trimp'][i-params[0]:i])
                ff_df['fatigue'][i] = sum(ff_df['b_trimp'][i-params[1]:i])
            
            if i == 0:
                ff_df['form'][i] = 0
            else:
                ff_df['form'][i] = ff_df['fatigue'][i-1]/ff_df['fitness'][i-1]
            
    return ff_df
    
def make_plot(ff_df):
    # Plot trimp over time
    plt.figure()
#    plt.plot(ff_df['date'], ff_df['b_trimp'],label='Banister TRIMP')
    plt.plot(ff_df['date'], ff_df['fatigue'],label='Fatigue')
    plt.plot(ff_df['date'], ff_df['fitness'],label='Fitness')
    plt.plot(ff_df['date'], ff_df['form'],label='Form')
    plt.hlines(0, ff_df['date'].loc[0], ff_df['date'].iloc[-1], linestyles='dashed')
    plt.vlines(ff_df['date'].iloc[-14],-500,500, linestyles='dashed')
    plt.title('Fitness-Fatigue model')
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2)
    plt.legend()
 
model = 'banister'
params = [42, 7] # [fitness, fatigue], [42, 7] as starting point
ff_df = create_ff_df(df_acts)

#ff_df = trimp_to_ff_df(trimp_df,ff_df)
#ff_df = ff_model(ff_df, params, model)
#make_plot(ff_df)
#plt.title(model)