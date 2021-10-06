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
    columns = ['banister_trimp', 'dis_speed_high', 'dis_speed_low', 'distance',
               'edwards_trimp', 'moving_time', 'lucia_trimp', 'lucia_trimp_speed',
               'trimp_norm_distance', 'trimp_norm_hr']
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

    return ff_df
    # return ff_df.drop(['fatigue','fitness'], axis=1)
  

def busso(ff_df, params, workload='distance'):
    '''
    Model the original banister equation on the input workload parameters

    Model equations according to equation 5/6 from
    Busso, T., Candau, R., & Lacour, J. (1994). Fatigue and fitness modelled from
    the effects of training on performance. European Journal of Applied Physiology
    and Occupational Physiology, 69(1), 50–54. https://doi.org/10.1007/BF00867927    
    
    This should be slightly different compared to banister (delay), but this
    implementation is not working for some reason...

    Input: ff_df : pandas.dataframe with days since first upload and aggregated
            workload per day.
            params : model parameters for decay of fitness and fatigue
            workload : name of the workload variable in ff_df

    output: ff_df with addition of banister_workload
    '''

    busso_workload = 'busso_' + workload

    ff_df['fitness'] = np.zeros(len(ff_df))
    ff_df['fatigue'] = np.zeros(len(ff_df))
    ff_df[busso_workload] = np.zeros(len(ff_df))

    for i in range(len(ff_df)):
        if i < 2:
            ff_df['fitness'][0] = 0 + ff_df[workload][0] * np.exp(-1/params[0])
            ff_df['fatigue'][0] = 0 + ff_df[workload][0] * np.exp(-1/params[1])
            ff_df[busso_workload][0] = 0
        else:
            ff_df['fitness'][i] = (ff_df['fitness'][i-2] + ff_df[workload][i-1]) * np.exp(-1/params[0])
            ff_df['fatigue'][i] = (ff_df['fatigue'][i-2] + ff_df[workload][i-1]) * np.exp(-1/params[1])
            ff_df[busso_workload][i] = ff_df['fitness'][i-1] - ff_df['fatigue'][i-1]
    
    return ff_df
    # return ff_df.drop(['fatigue','fitness'], axis=1)


def banister(ff_df, params, workload='distance'):
    '''
    Model the original banister equation on the input workload parameters

    Model equations according to equation 10/11 from
    B. S. Hemingway, L. Greig, and P. Swinton, “A NARRATIVE REVIEW OF
    MATHEMATICAL FITNESS-FATIGUE MODELLING FOR APPLICATIONS IN EXERCISE
    SCIENCE: MODEL DYNAMICS, METHODS, LIMITATIONS, AND FUTURE
    RECOMMENDATIONS A,” 2020, doi: 10.31236/osf.io/ap75j.

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

    return ff_df
    # return ff_df.drop(['fatigue', 'fitness'], axis=1)


def calvert(ff_df, workload='distance'):
    '''
    Model the original Calvert (1976) equation on the input workload parameters
    using the three-component model

    See:
    Calvert, T. W., Banister, E. W., Savage, M. V., & Bach, T. (1976). A Systems
    Model of the Effects of Training on Physical Performance. IEEE Transactions
    on Systems, Man and Cybernetics, SMC-6(2), 94–102.
    https://doi.org/10.1109/TSMC.1976.5409179

    Model parameters are set

    Input: ff_df : pandas.dataframe with days since first upload and aggregated
            workload per day.
            workload : name of the workload variable in ff_df

    output: ff_df with addition of calvert_workload
    '''
    tau_1 = 50
    tau_2 = 5
    tau_3 = 15
    K = 2  # Also the value of 10 is mentioned

    calvert_workload = 'calvert_' + workload

    ff_df['fitness_1'] = np.zeros(len(ff_df))
    ff_df['fitness_2'] = np.zeros(len(ff_df))
    ff_df['fitness'] = np.zeros(len(ff_df))
    ff_df['fatigue'] = np.zeros(len(ff_df))
    ff_df[calvert_workload] = np.zeros(len(ff_df))

    for i in range(len(ff_df)):
        if i == 0:
            ff_df['fitness_1'][0] = 0 + (ff_df[workload][0])
            ff_df['fitness_2'][0] = 0 + (ff_df[workload][0])
            ff_df['fitness'][0] = ff_df['fitness_1'][0] - ff_df['fitness_2'][0]
            ff_df['fatigue'][0] = 0 + (ff_df[workload][0])
            ff_df[calvert_workload][0] = 0
        else:
            ff_df['fitness_1'][i] = ff_df['fitness_1'][i-1]*(np.exp(-1/tau_1)) + ff_df[workload][i]
            ff_df['fitness_2'][i] = ff_df['fitness_2'][i-1]*(np.exp(-1/tau_2)) + ff_df[workload][i]
            ff_df['fitness'][i] = ff_df['fitness_1'][i] - ff_df['fitness_2'][i]
            ff_df['fatigue'][i] = ff_df['fatigue'][i-1]*(np.exp(-1/tau_3)) + ff_df[workload][i]
            ff_df[calvert_workload][i] = ff_df['fitness'][i-1] - K*ff_df['fatigue'][i-1]

    return ff_df.drop(['fitness_1', 'fitness_2'], axis=1)
    # return ff_df


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

    return ff_df # ff_df.drop(['AL','CL'], axis=1)


def make_plot(ff_df):
    # Plot trimp over time
    plt.figure()
#    plt.plot(ff_df['date'], ff_df['b_trimp'],label='Banister TRIMP')
    plt.plot(ff_df.index, ff_df['fatigue'], label='Fatigue')
    plt.plot(ff_df.index, ff_df['fitness'], label='Fitness')
    plt.plot(ff_df.index, ff_df['form'], label='Form')
#    plt.hlines(0, ff_df.index.loc[0], ff_df['date'].iloc[-1], linestyles='dashed')
#    plt.vlines(ff_df['Index'].iloc[-14],-500,500, linestyles='dashed')
    plt.title('Fitness-Fatigue model')
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2)
    plt.legend()


model = 'banister'
workload = 'banister_trimp'
params = [42, 7]  # [fitness, fatigue], [42, 7] as starting point
ff_df = create_ff_df(df_acts)
ff_df = trainingspeaks(ff_df, params, 'impulse')
ff_df = calvert(ff_df, 'banister_trimp')

plt.plot(ff_df['calvert_banister_trimp'], label='form')
plt.plot(ff_df['fitness'], label='fitness')
plt.plot(ff_df['fatigue'], label='fatigue')
plt.xticks(rotation=45)
plt.subplots_adjust(bottom=0.2)
plt.legend()