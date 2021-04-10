import tools.DataHandler as dh
import tools.authorization as auth
import tools.segments as seg
import os
import time
import json
import tools.ActivityHandler as ah

if __name__ == '__main__':
    # Check if user_access token is available, otherwise do authorisation first.
    if not os.path.isfile(os.path.join('tokens', 'user_access.token')):
        auth.authorize()
    with open(os.path.join('tokens', 'user_access.token'), 'r') as file:
        user_token = json.load(file)
    # Check if token is still valid, otherwise refresh token
    if time.time() > user_token['expires_at']:
        user_token = auth.refresh(user_token['refresh_token'])
        print('Token refreshed')
    access_token = user_token['access_token']

    # Create dataHandler object
    data = dh.DataHandler(access_token, 'data')
    # Get latest data
    data.sync()
    df = data.get_data()
    
    acts = ah.ActivityHandler(access_token, 'data')
    acts.sync(force=True)
    df_acts = acts.get_data()

    # Start code specific for Data Science course
    df_acts = df_acts[df_acts['type']=='Run']