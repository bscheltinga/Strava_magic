from stravalib import Client
from tqdm import tqdm
import pandas as pd

class DataHandler(object):
    def __init__(self, token, datapath):
        self.__token = token
        self.__datapath = datapath

        #Initialize client
        self.__connect(token)

    def __connect(self, token):
        self.__api = Client(access_token=token)

    def __handleActivity(self, activity):
        datarow = {'average_speed' : float(activity.average_speed),
                   'comment_count' : int(activity.comment_count),
                   'distance' : float(activity.distance),
                   'elapsed_time' : str(activity.elapsed_time),
                   'flagged' : str(activity.flagged),
                   'id' : int(activity.id),
                   'kudos_count': int(activity.kudos_count),
                   'max_speed' : float(activity.max_speed),
                   'moving_time' : str(activity.moving_time),
                   'name': str(activity.name),
                   'pr_count' : int(activity.pr_count),
                   'total_photo_count' : int(activity.total_photo_count),
                   'type' : str(activity.type),
                   'start_date' : str(activity.start_date)
                   }
        return datarow

    def full_sync(self):
        df = pd.DataFrame()
        activities = self.__api.get_activities(limit=8)
        for activity in tqdm(activities):
            entry = self.__handleActivity(activity)
            df = df.append(entry, ignore_index=True)
        df.to_excel('test.xlsx')

# This code wil be removed, now for testing the object

with open(r'tokens\user_access.token', 'r') as file:
    user_token = file.read()
data = DataHandler(user_token,  '')
data.full_sync()


