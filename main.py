import tools.DataHandler as dh
import tools.analytics as anal
import tools.authorization as auth
import tools.kmlmap as kmlmap
import os
import time
import json




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
    # Show totals per sport
    print('=====Totals=====')
    totals = anal.totals(df)
    time = str(totals['elapsed_time'])
    print('totals: distance={:.2f}, kudos={}, avg_kudos={:.2f}, elapsed time={}'.format(totals['distance'],
                                                                                         totals['kudos'],
                                                                                         totals['avg_kudos'], time))
    # Show h-index of dataset
    print('=====H-Index=====')
    h = anal.h_index(df)
    print("H-index overall: %i" % h)
    anal.trindex(df)
    # Calculate average speed
    print('=====Average speed=====')
    avg_speed_bike = anal.avg_speed(df.loc[df['type'] == 'Ride'])
    avg_speed_run = anal.avg_speed(df.loc[df['type'] == 'Run'])
    print("Average speed bike: %.2f km/h" % avg_speed_bike)
    print("Average speed run: %.2f km/h" % avg_speed_run)
    # Hot hours
    print('=====Hot hours=====')
    anal.hothours(df)

    #Create KML map for heatmap
    # kmlmap.create_kml(access_token, df.loc[df['type'] == 'Ride'])


