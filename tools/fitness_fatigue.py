# Implementation of fitness fatigue model
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
# assuming act. has HR_data
# b_trimp: implementation of Banister' trimp (avg_hr*duration)


def b_trimp(df):
    df = df.loc[df['has_heartrate'] == True]
    b_trimps = (df['moving_time'] / np.timedelta64(1, 'h')) * df['average_heartrate']
    return b_trimps

def create_ff_df(df):
    ff_df = pd.DataFrame()
    start = df.index[0]
    start = datetime.fromtimestamp(start.timestamp())
    end = datetime.today() + datetime.timedelta(days=14)
    days = ((end-start).days)+1
    datelist = pd.date_range(start, periods=days).tolist()
    ff_df['date'] = datelist
    
    return ff_df

def trimp_to_ff_df (b_trimps,ff_df):
    # loop over all dates in df
    # does not work for multiple activities on one day
    ff_df['b_trimp'] = np.zeros(len(ff_df))
    j = 0
    for i in range(len(b_trimps)):
        flag=True
        while flag == True:
            if b_trimps.index[i].date() == ff_df['date'][j].date():
                ff_df['b_trimp'][j] = ff_df['b_trimp'][j] + b_trimps[i]
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
            ff_df['fitness'][0] = 0 + (ff_df['b_trimp'][0] - 0)*(1-np.exp(-1/42))
            ff_df['fatigue'][0] = 0 + (ff_df['b_trimp'][0] - 0)*(1-np.exp(-1/7))
            ff_df['form'][0] = 0
        else:
            ff_df['fitness'][i] = ff_df['fitness'][i-1] + (ff_df['b_trimp'][i] - ff_df['fitness'][i-1])*(1-np.exp(-1/42))
            ff_df['fatigue'][i] = ff_df['fatigue'][i-1] + (ff_df['b_trimp'][i] - ff_df['fatigue'][i-1])*(1-np.exp(-1/7))
            ff_df['form'][i] = ff_df['fitness'][i-1] - ff_df['fatigue'][i-1]
            
    
def make_plot(ff_df):
    # Plot trimp over time
    plt.figure()
    plt.plot(ff_df['date'], ff_df['b_trimp'],label='Banister TRIMP')
    plt.plot(ff_df['date'], ff_df['fatigue'],label='Fatigue')
    plt.plot(ff_df['date'], ff_df['fitness'],label='Fitness')
    plt.plot(ff_df['date'], ff_df['form'],label='Form')
    plt.hlines(0, ff_df['date'].loc[0], ff_df['date'].iloc[-1], linestyles='dashed')
    plt.vlines(ff_df['date'].iloc[-14],-500,500, linestyles='dashed')
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2)
    plt.legend()