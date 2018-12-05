import tools.DataHandler as dh
import tools.analytics as anal
import tools.authorization as auth
import os
#Check if user_access token is available, otherwise do authorisation first.
if not os.path.isfile(r'tokens\user_access.token'):
   auth.authorize()
with open(r'tokens\user_access.token', 'r') as file:
    user_token = file.read()
# create dataHandler object
data = dh.DataHandler(user_token,  'data')
# Get latest data
data.sync()
df = data.get_data()

# Calculate H-index for sports
for sport in ['Ride', 'Run', 'Swim']:
    df_sport = df.loc[df['type'] == sport]
    totals = anal.totals(df_sport)
    h_sport = anal.h_index(df_sport, figures=False)
    print('%s h-index: %i' %(sport, h_sport))
    time = str(totals['elapsed_time'])
    print('{} totals: distance={:.2f}, kudos={}, avg_kudos={:.2f}, elapsed time={}'.format(sport, totals['distance'], totals['kudos'], totals['avg_kudos'], time))

