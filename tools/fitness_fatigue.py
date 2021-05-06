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
    - Set the workload parameters from df_acts in ff_df.
    - Set 0 it no activity was done.
    - Sum the values for multiple activities on one day.
    
    Input: pandas.dataframe with workloads per activity date.
    
    Output: pandas.dataframe with days since first upload and aggregated
            workload per day.
    '''
    columns = ['banister_trimp','dis_speed_high','dis_speed_low','distance',
               'edwards_trimp','moving_time','lucia_trimp','lucia_trimp_speed',
               'trimp_norm_distance','trimp_norm_hr']
    ff_df = df_acts.resample('D', on='start_date')[columns].sum()

    return ff_df

def trainingspeaks(ff_df, params, workload='distance'):
    '''
    Model the trainingspeaks equation on the input workload parameters
    
    Input: ff_df : pandas.dataframe with days since first upload and aggregated
            workload per day.
            params : model parameters for decay of fitness and fatigue
            workload : name of the workload variable in ff_df
            
    output: ff_df with addition of trainingspeaks_workload
    '''
    trainingspeaks_workload = 'trainingspeaks_' + workload
    
    ff_df['fitness'] = np.zeros(len(ff_df))
    ff_df['fatigue'] = np.zeros(len(ff_df))
    ff_df[trainingspeaks_workload] = np.zeros(len(ff_df))
    
    for i in range(len(ff_df)):
            if i == 0:
                ff_df['fitness'][0] = 0 + (ff_df[workload][0] - 0)*(1-np.exp(-1/params[0]))
                ff_df['fatigue'][0] = 0 + (ff_df[workload][0] - 0)*(1-np.exp(-1/params[1]))
                ff_df[trainingspeaks_workload][0] = 0
            else:
                ff_df['fitness'][i] = ff_df['fitness'][i-1] + (ff_df[workload][i] - ff_df['fitness'][i-1])*(1-np.exp(-1/params[0]))
                ff_df['fatigue'][i] = ff_df['fatigue'][i-1] + (ff_df[workload][i] - ff_df['fatigue'][i-1])*(1-np.exp(-1/params[1]))
                ff_df[trainingspeaks_workload][i] = ff_df['fitness'][i-1] - ff_df['fatigue'][i-1]
    
    return ff_df.drop(['fatigue','fitness'], axis=1)

def banister(ff_df, params, workload='distance'):
    '''
    Model the original banister equation on the input workload parameters
    
    Model equations according to equation 10/11 from
    B. S. Hemingway, L. Greig, and P. Swinton, “A NARRATIVE REVIEW OF MATHEMATICAL FITNESS-FATIGUE MODELLING FOR APPLICATIONS IN EXERCISE SCIENCE: MODEL DYNAMICS, METHODS, LIMITATIONS, AND FUTURE RECOMMENDATIONS A,” 2020, doi: 10.31236/osf.io/ap75j.
    fitness/fatigue = Value yesterday*exp(param) + workload
    
    Input: ff_df : pandas.dataframe with days since first upload and aggregated
            workload per day.
            params : model parameters for decay of fitness and fatigue
            workload : name of the workload variable in ff_df
            
    output: ff_df with addition of banister_workload
    '''
    
    banister_workload = 'banister_' + workload
    
    ff_df['fitness'] = np.zeros(len(ff_df))
    ff_df['fatigue'] = np.zeros(len(ff_df))
    ff_df[banister_workload] = np.zeros(len(ff_df))
    
    for i in range(len(ff_df)):
        if i == 0:
            ff_df['fitness'][0] = 0 + (ff_df[workload][0])
            ff_df['fatigue'][0] = 0 + (ff_df[workload][0])
            ff_df[banister_workload][0] = 0
        else:
            ff_df['fitness'][i] = ff_df['fitness'][i-1]*(np.exp(-1/params[0])) + ff_df[workload][i]
            ff_df['fatigue'][i] = ff_df['fatigue'][i-1]*(np.exp(-1/params[1])) + ff_df[workload][i]
            ff_df[banister_workload][i] = ff_df['fitness'][i-1] - ff_df['fatigue'][i-1]
            
    return ff_df.drop(['fatigue','fitness'], axis=1)

def ACWR(ff_df, params, workload):
    '''
    Model the acute:chronice workload ratio (ACWR)
    
    Input: ff_df : pandas.dataframe with days since first upload and aggregated
            workload per day.
            params : model parameters for decay of fitness and fatigue
            workload : name of the workload variable in ff_df
            
    output: ff_df with addition of acwr_workload
    '''    
    ACWR_workload = 'ACWR_' + workload
    
    ff_df['CL'] = np.zeros(len(ff_df))
    ff_df['AL'] = np.zeros(len(ff_df))
    ff_df[ACWR_workload] = np.zeros(len(ff_df))

    for i in range(len(ff_df)):
        if i <= params[0] and i <= params[1]:
            ff_df['CL'][i] = sum(ff_df[workload][0:i])
            ff_df['AL'][i] = sum(ff_df[workload][0:i])
            
        elif i <= params[0] and i > params[1]:
            ff_df['CL'][i] = sum(ff_df[workload][0:i])
            ff_df['AL'][i] = sum(ff_df[workload][i-params[1]:i])
            
        else:
            ff_df['CL'][i] = sum(ff_df[workload][i-params[0]:i])/4
            ff_df['AL'][i] = sum(ff_df[workload][i-params[1]:i])
        
        if i == 0:
            ff_df[ACWR_workload][i] = 0
        else:
            ff_df[ACWR_workload][i] = ff_df['AL'][i-1]/ff_df['CL'][i-1]
            
    return ff_df.drop(['AL','CL'], axis=1)

def AL(ff_df, params, workload):
    '''
    Model the acute load
    
    Input: ff_df : pandas.dataframe with days since first upload and aggregated
            workload per day.
            params : model parameters number of days of acute load
            workload : name of the workload variable in ff_df
            
    output: ff_df with addition of al_workload
    '''    
    AL_workload = 'AL_' + workload
    
    ff_df['CL'] = np.zeros(len(ff_df))
    ff_df['AL'] = np.zeros(len(ff_df))
    ff_df[AL_workload] = np.zeros(len(ff_df))

    for i in range(len(ff_df)):
        if i <= params[0] and i <= params[0]:
            ff_df[AL_workload][i] = sum(ff_df[workload][0:i])
            
        elif i <= params[0] and i > params[0]:
            ff_df[AL_workload][i] = sum(ff_df[workload][i-params[0]:i])
            
        else:
            ff_df[AL_workload][i] = sum(ff_df[workload][i-params[0]:i])
        
            
    return ff_df
    
def make_plot(ff_df):
    # Plot trimp over time
    plt.figure()
#    plt.plot(ff_df['date'], ff_df['b_trimp'],label='Banister TRIMP')
    plt.plot(ff_df.index, ff_df['fatigue'],label='Fatigue')
    plt.plot(ff_df.index, ff_df['fitness'],label='Fitness')
    plt.plot(ff_df.index, ff_df['form'],label='Form')
#    plt.hlines(0, ff_df.index.loc[0], ff_df['date'].iloc[-1], linestyles='dashed')
#    plt.vlines(ff_df['Index'].iloc[-14],-500,500, linestyles='dashed')
    plt.title('Fitness-Fatigue model')
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2)
    plt.legend()
 
model = 'ACWR'
workload = 'distance'
params = [28, 7] # [fitness, fatigue], [42, 7] as starting point
ff_df = create_ff_df(df_acts)
ff_df = ACWR(ff_df, params, 'distance')

# plt.plot(ff_df['ACWR_distance'])
# plt.xticks(rotation=45)
# plt.subplots_adjust(bottom=0.2)
# #plt.title(model)