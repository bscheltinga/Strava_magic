# Implementation of fitness fatigue model
# assuming act. has HR_data
# b_trimp: implementation of Banister' trimp (avg_hr*duration)


def b_trimp(df):
    df = df.loc[df['has_heartrate'] == True]
    b_trimps = (df['moving_time'] / np.timedelta64(1, 'h')) * df['average_heartrate']
