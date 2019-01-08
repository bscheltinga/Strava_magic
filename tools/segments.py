import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import os.path
from stravalib import Client

def segmentlist(user_token, df):
    client = Client(access_token=user_token)
    df_segments = pd.DataFrame()
    idx = 0
    for a, row in tqdm(df.iterrows(), total=df.shape[0],desc='Creating all segments list'):
        if idx % 550 == 0 and idx > 1:  # To prevent exceeding strava limits
            print('Waiting for STRAVA API limits.')
            time.sleep(900)
        id = row['id']

        # Get from each activity the ridden/ran segments
        last_act = client.get_activity(activity_id= id, include_all_efforts=True)
        for i in range(len(last_act.segment_efforts)):
            entry = {'id' : last_act.segment_efforts[i].segment.id,
                     'name' : last_act.segment_efforts[i].name}
            df_segments = df_segments.append(entry, ignore_index=True)
        idx += 1
        if idx == 50:
            break
    df_segments = df_segments.drop_duplicates()
    df_segments.to_excel(r'data\Segments.xlsx')
    return df_segments
    # To get the segment standings:
    #segment = client.get_segment_leaderboard(segment_id=segment_id, gender='M') # Gender 'M'???