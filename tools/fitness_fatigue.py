# Implementation of fitness fatigue model
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# assuming act. has HR_data
# b_trimp: implementation of Banister' trimp (avg_hr*duration)
# other trimp methods could be implemented
# gains for fitness and fatigue could be implemented
# delay in fitness response could be implemented.

def b_trimp(df):
    trimp_df = pd.DataFrame()
    df = df.loc[df['has_heartrate'] == True]
    trimp_df['date'] = df['start_date']
    trimp_df['trimp'] = (df['moving_time'] / np.timedelta64(1, 'h')) * df['average_heartrate']
    trimp_df = trimp_df.reset_index(drop=True)
    return trimp_df

def create_ff_df(df):
    df = df.loc[df['has_heartrate'] == True]
    ff_df = pd.DataFrame()
    start = df.index[0]
    start = df['start_date'][start]
    start = datetime.fromtimestamp(start.timestamp())
    end = datetime.today()
    days = ((end-start).days)+15 # add some days for future view
    datelist = pd.date_range(start, periods=days).tolist()
    ff_df['date'] = datelist
    
    return ff_df

def trimp_to_ff_df (trimp_df,ff_df):
    # loop over all dates in df
    # does not work for multiple activities on one day
    ff_df['b_trimp'] = np.zeros(len(ff_df))
    j = 0
    for i in range(len(trimp_df)):
        flag=True
        while flag == True:
            if trimp_df['date'][i].date() == ff_df['date'][j].date():
                ff_df['b_trimp'][j] = ff_df['b_trimp'][j] + trimp_df['trimp'][i]
                flag = False
            else:
                j += 1                
    return ff_df

def ff_model(ff_df,params):
    ff_df['fitness'] = np.zeros(len(ff_df))
    ff_df['fatigue'] = np.zeros(len(ff_df))
    ff_df['form'] = np.zeros(len(ff_df))
    
    for i in range(len(ff_df)):
        if i == 0:
            ff_df['fitness'][0] = 0 + (ff_df['b_trimp'][0] - 0)*(1-np.exp(-1/params[0]))
            ff_df['fatigue'][0] = 0 + (ff_df['b_trimp'][0] - 0)*(1-np.exp(-1/params[1]))
            ff_df['form'][0] = 0
        else:
            ff_df['fitness'][i] = ff_df['fitness'][i-1] + (ff_df['b_trimp'][i] - ff_df['fitness'][i-1])*(1-np.exp(-1/params[0]))
            ff_df['fatigue'][i] = ff_df['fatigue'][i-1] + (ff_df['b_trimp'][i] - ff_df['fatigue'][i-1])*(1-np.exp(-1/params[1]))
            ff_df['form'][i] = ff_df['fitness'][i-1] - ff_df['fatigue'][i-1]
            
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
    
params = [42, 7] # fatigue effect for 7 and fitness effect for 42 days.
trimp_df = b_trimp(df)
ff_df = create_ff_df(df)
ff_df = trimp_to_ff_df (trimp_df,ff_df)

ff_df = ff_model(ff_df,params)
make_plot(ff_df)