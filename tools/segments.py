import numpy as np
import pandas as pd
import time
from stravalib import Client

def segmentlist(user_token, df):
    client = Client(access_token=user_token)
    df_segments = pd.DataFrame()
    df_segments['id'] = np.nan # make the id column
    idx = 0
    i_lim = 1 # For the limit counter
    limit_count = 0
    for a, row in df.iterrows():
        id = float(row['id']) # Make float to compare with the DF
        last_act = client.get_activity(activity_id=id, include_all_efforts=True) # Get activity

        for i in range(len(last_act.segment_efforts)):
            segment_id = last_act.segment_efforts[i].segment.id
            if (last_act.segment_efforts[i].segment.hazardous == 0 and
                    sum(df_segments['id'].isin([segment_id])) == 0):  # Only for unique segments
                print('Activities: %i / %i | Segments: %i / %i | Limits: %i' %
                      (idx, len(df), i, len(last_act.segment_efforts),limit_count))
                entry = {'id': int(last_act.segment_efforts[i].segment.id),
                         'name': last_act.segment_efforts[i].name,
                         'distance': float(last_act.segment_efforts[i].distance.num),
                         'activity_type': str(last_act.type),
                         'average_grade': last_act.segment_efforts[i].segment.average_grade,
                         'efforts': last_act.segment_efforts[i].segment.leaderboard.effort_count,
                         'KOM_time': last_act.segment_efforts[i].segment.leaderboard.entries[1].elapsed_time
                         }


                for j in reversed(range(len(last_act.segment_efforts[i].segment.leaderboard.entries))):
                    if str(last_act.segment_efforts[i].segment.leaderboard.entries[j].athlete_name) == 'Bouke S.':
                        entry['rank'] = last_act.segment_efforts[i].segment.leaderboard.entries[j].rank
                        entry['elapsed_time'] = last_act.segment_efforts[i].segment.leaderboard.entries[
                            j].elapsed_time
                        entry['pr_date'] = last_act.segment_efforts[i].segment.leaderboard.entries[
                            j].start_date_local
                        break

                df_segments = df_segments.append(entry, ignore_index=True)
                limit_count = len(df_segments) + idx  # Found that 1 for each unique seg and 1 for each act.
                entry = []

                if limit_count > (580*i_lim):  # To prevent exceeding strava limits
                    LimitFlag = 1
                    i_lim += 1
                    print('Waiting for STRAVA API limits.')
                    while LimitFlag == 1:
                        time.sleep(20) # Wait 30 seconds
                        checktime = time.localtime()
                        if checktime.tm_min % 15 == 0:
                            LimitFlag = 0

        idx += 1
        if idx == 99999:  # Only first 1500 activities
            break

    df_segments['Perc_rank'] = (df_segments['rank'] / df_segments['efforts'])*100
    df_segments['distance'] = df_segments['distance']/1000
    df_segments['GosCore'] = -np.log10(df_segments['rank'] / df_segments['efforts'])
    df_segments['GosCore_max'] = -np.log10(1 / df_segments['efforts'])
    #df_segments['seconds'] = pd.to_timedelta(df_segments['elapsed_time'])
    #df_segments['seconds'] = pd.Series.dt.total_seconds(df_segments['seconds'])
    #df_segments['Avg_speed'] = # km/h
    #df_segments['Avg_pace'] = # min/km

    #Calculate GosCore
    df_segments.to_excel(r'data\Segments.xlsx')
    df_segments = df_segments.sort_values(by=['GosCore'],ascending=False)
    GosCore = df_segments['GosCore'].cumsum()
    GosCore_max = df_segments['GosCore_max'].cumsum()
    if len(GosCore) > 98:
        print('GosCore: %.2f out of %.2f' % ( round(GosCore.values[99]/100,2),round(GosCore_max.values[99]/100,2)))
    else:
        index = int(len(GosCore)-1)
        print(
            'GosCore: %.2f out of %.2f' % (round(GosCore.values[index] / (index+1), 2)
                                           , round(GosCore_max.values[index] / (index+1), 2)))
    df_segments.to_excel(r'data\Segmentsv2.xlsx')
    df_segments.to_excel(r'data\Segments.xlsx')


    return df_segments

# TO ADD: avg speed, avg pace, goscore