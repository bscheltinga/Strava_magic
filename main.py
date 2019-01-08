import tools.DataHandler as dh
import tools.analytics as anal
import tools.authorization as auth
import tools.kmlmap as kmlmap
import os
import time
import pandas as pd
import json

def hindex(df):
    # Calculate totals for sports
    for sport in ['Ride', 'Run', 'Swim']:
        df_sport = df.loc[(df['type'] == sport) & (df['private'] == False)]
        totals = anal.totals(df_sport)
        time = str(totals['elapsed_time'])
        print(
            '{} totals: distance={:.2f}, kudos={}, avg_kudos={:.2f}, elapsed time={}'.format(sport, totals['distance'],
                                                                                             totals['kudos'],
                                                                                             totals['avg_kudos'], time))
    # Calculate H-index per day for sports
    for sport in ['Ride', 'Run', 'Swim']:
        df_day = df.loc[(df['type'] == sport)]
        df_day.index = pd.to_datetime(df_day['start_date'])
        df_day = df_day.resample('D').sum()
        df_day = df_day.drop(df_day.loc[df_day['distance'] == 0].index)
        h_sport = anal.h_index(df_day, figures=False)
        print('%s day h-index: %i' % (sport, h_sport))

    # Calculate tri H-index, a.k.a. H-Trindex
    df.index = pd.to_datetime(df['start_date'])
    df = df.resample('D').sum()
    df = df.drop(df.loc[df['distance'] == 0].index)
    h_sport = anal.h_index(df, figures=False)
    print('H-Trindex: %i' % (h_sport))

############MAIN###############

if __name__ == '__main__':
    # Check if user_access token is available, otherwise do authorisation first.
    if not os.path.isfile(r'tokens\user_access.token'):
       auth.authorize()
    with open(r'tokens\user_access.token', 'r') as file:
        user_token = json.load(file)
    # Check if token is still valid, otherwise refresh token
    if time.time() > user_token['expires_at']:
        user_token = auth.refresh(user_token['refresh_token'])
        print('Token refreshed')
    access_token = user_token['access_token']

    # Create dataHandler object
    data = dh.DataHandler(access_token,  'data')
    # Get latest data
    data.sync()
    df = data.get_data()
    # Show h-index of dataset
    hindex(df)

    #Create KML map for heatmap
    # kmlmap.create_kml(access_token, df.loc[df['type'] == 'Ride'])


