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

    df_segments = df_segments.drop_duplicates()
    df_segments.to_excel(r'data\Segments.xlsx')
    return df_segments

# Later, make one function which combines segmentlist and segmentrating
def segmentrating(user_token, df_segments):
    client = Client(access_token=user_token)
    for idx in range(20) # len(df_segments) but for no, only first 20 segments
        client. # get segments by number