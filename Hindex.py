# 1-12-2018 Calculate H-index from run and rides.
import stravalib
from stravalib.client import Client
  # import pprint
import numpy as np
import matplotlib.pyplot as plt

# Strava tokens
TOKEN = "123abc"  # Token here
client = Client(access_token=TOKEN)

# Variables
Act_count = [10]

# Pre allocate the arrays
athlete_count = []
average_heartrate = []
average_speed = []
comment_count = []
date = [] # ADD THIS
distance = []
elapsed_time = []
flagged = []
id = []
kudos_count = []
max_heartrate = []
max_speed = []
moving_time = []
name = []
pr_count = []
total_photo_count = []
start_time = [] # ADD THIS
type = []

activities = client.get_activities(limit=Act_count)
for activity in activities:

    # Here all the data that is wished to be saved
    athlete_count.append(float("{0.athlete_count}".format(activity)))
    if "{0.average_heartrate}".format(activity) == 'None':
        average_heartrate.append("{0.average_heartrate}".format(activity))
        max_heartrate.append("{0.max_heartrate}".format(activity))
    else:
        average_heartrate.append(float("{0.average_heartrate}".format(activity)))
        max_heartrate.append(float("{0.max_heartrate}".format(activity)))

    average_speed.append(float("{0.average_speed.num}".format(activity)))
    comment_count.append(float("{0.comment_count}".format(activity)))
    distance.append(float("{0.distance.num}".format(activity)))
    elapsed_time.append(float("{0.elapsed_time.seconds}".format(activity)))
    flagged.append("{0.flagged}".format(activity))
    id.append(float("{0.id}".format(activity)))
    kudos_count.append(float("{0.kudos_count}".format(activity)))
    max_speed.append(float("{0.max_speed.num}".format(activity)))
    moving_time.append(float("{0.moving_time.seconds}".format(activity)))
    name.append("{0.name}".format(activity))
    pr_count.append(float("{0.pr_count}".format(activity)))
    total_photo_count.append(float("{0.total_photo_count}".format(activity)))
    type.append("{0.type}".format(activity))

distance = np.divide(distance, 1000)  # Set to km


'''
Data is now available. Might be an idea to save this later. For now, try to
get only the 'Ride' or 'Run' activities and calculate the H-index
'''

H_index_type = 'Run' # Run or ride here
H_index_distance = []
for i in range(len(type)):
    if type[i] == H_index_type:
        H_index_distance.append(distance[i])

# Determine the H-index
H_index_distance = sorted(H_index_distance, reverse=True)
for i in range(len(H_index_distance)):
    if i > H_index_distance[i]:
        H_index = i-1  # Outputs the H_index
        print(H_index)
        break

plt.figure()
plt.hist(H_index_distance)  # Tweak these parameters
plt.xlabel('Kilometers')
plt.ylabel('Activity count')
plt.title('Histogram of activities')

# Calculate the amount of activities for each bin
H_index_cum = []
for i in range(int(max(H_index_distance))):
    H_index_cum.append(sum(j > (i + 1) for j in H_index_distance))

plt.figure()
plt.bar(x=np.add(list(range(0, int(max(H_index_distance)))),1),height=H_index_cum)
plt.plot([0, max(H_index_distance)], [0, max(H_index_distance)],'r')  # Add the H-Index line
plt.xlabel('Kilometers')
plt.ylabel('Activity count')
plt.title('Cumulative histogram')

# Show plots
plt.show()
