# from __future__ import print_function
import stravalib
from stravalib.client import Client
# import pandas as pd
from pprint import pprint
import simplekml
import numpy as np
import time


# Variables
Act_count = 50  # Number of activities
alltypes = ['AlpineSki', 'BackcountrySki', 'Canoeing', 'Crossfit', 'EBikeRide', 'Elliptical', 'Handcycle', 'Hike', 'IceSkate', 'InlineSkate', 'Kayaking', 'Kitesurf', 'NordicSki', 'Ride', 'RockClimbing', 'RollerSki', 'Rowing', 'Run', 'Snowboard', 'Snowshoe', 'StairStepper', 'StandUpPaddling', 'Surfing', 'Swim', 'VirtualRide', 'VirtualRun', 'Walk', 'WeightTraining', 'Wheelchair', 'Windsurf', 'Workout', 'Yoga']  # Preallocation
Type = alltypes  # ['Run']  # use all types of activities
types = ['latlng']  # types for streams
beforeUTC = None  # '2017-06-01T00:00:00Z'.
afterUTC = None  # '2017-06-01T00:00:00Z'
leave_out = '[]'  # number of activities to leave out

# Strava tokens
TOKEN = "123abc"  #  Your STRAVA token here
client = Client(access_token=TOKEN)

# Data arrays
IDs = []
Titles = []
Types = []

# Initiate KML
kml = simplekml.Kml()

''''
PART I: get the activities in a list.
'''
for activity in client.get_activities(limit=Act_count, before=afterUTC, after=beforeUTC):
    print("{0.id} {0.type} {0.name} {0.manual}".format(activity))
    if "{0.start_latlng}".format(activity) == 'None':
        print('No GPS for {0.name}'.format(activity))

    elif "{0.manual}".format(activity) == 'True':
        print('No GPS for {0.name}'.format(activity))

    elif "{0.type}".format(activity) not in Type:
        print('Wrong activity type for {0.name}'.format(activity))

    elif "{0.id}".format(activity) in leave_out:
        print('{0.name}'.format(activity), 'in leave out list')
    else:
        IDs.append("{0.id}".format(activity))
        Titles.append("{0.name}".format(activity))
    #    Types.append("{0.type}".format(activity))

# pprint(IDs)
pprint(Titles)
# pprint(Types)
print('Get streams and print save to KML')

''''
PART II: get the activity stream and add it to the kml
'''
for x in range(len(IDs)):
    if x % 500 == 0 and x > 1:  # To prevent exceeding strava limits
        print('Waiting for STRAVA API limits. Get a coffee!')
        print(time.localtime())
        time.sleep(900)

    print(x, Titles[x])
    streams = client.get_activity_streams(IDs[x], types=types, resolution='medium')
    cords = (streams['latlng'].data)
    cords = np.array(cords)
    cords = np.flip(cords)  # Flip the cords for right kml notation

    ls = kml.newlinestring(name=Titles[x])
    ls.coords = cords
    ls.extrude = 1

kml.save("KMLmap.kml")
