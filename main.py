import tools.DataHandler as dh
import tools.analytics as anal
with open(r'tokens\user_access.token', 'r') as file:
    user_token = file.read()
# create dataHandler object
data = dh.DataHandler(user_token,  'data')
# Get latest data
data.sync()
df = data.get_data()
# Calculate H-index for rides
df_ride = df.loc[df['type'] == 'Ride']
anal.h_index(df_ride, figures=False)

# Calculate H-index for runs
df_run = df.loc[df['type'] == 'Run']
anal.h_index(df_run, figures=False)
