import tools.DataHandler as dh
import tools.authorization as auth
import tools.stat_collector as stat
import tools.selectdata as selectdata
import tools.kmlmap as kmlmap
import os
import time
import json




############MAIN###############

if __name__ == '__main__':
    # Check if user_access token is available, otherwise do authorisation first.
    if not os.path.isfile(os.path.join('tokens','user_access.token')):
       auth.authorize()
    with open(os.path.join('tokens','user_access.token'), 'r') as file:
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

    # Select data
    year_df, year_headers = selectdata.year(df)
    sport_df, sport_headers = selectdata.sport(df)
    gear_df, gear_headers = selectdata.gear(df)
    # Collect statistics from selected data
    stat_df = stat.collect(year_df, year_headers)
    stat.output(stat_df, 'year.xlsx')
    stat_df = stat.collect(sport_df, sport_headers)
    stat.output(stat_df, 'sport.xlsx')
    stat_df = stat.collect(gear_df, gear_headers)
    stat.output(stat_df, 'gear.xlsx')

    #Create KML map for heatmap
    # kmlmap.create_kml(access_token, df.loc[df['type'] == 'Ride'])


