# Implementation of fitness fatigue model
from datetime import datetime
import pandas as pd
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
    end = datetime.today()
    days = ((end-start).days)+1
    datelist = pd.date_range(start, periods=days).tolist()
    ff_df['date'] = datelist
    
    return ff_df

def trimp_to_ff_df (b_trimps,ff_df):
    
def make_plot(b_trimps)
    # Plot trimp over time
    plt.plot(b_trimps.index, b_trimps)
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2)