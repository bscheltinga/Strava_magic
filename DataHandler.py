from stravalib import Client
from tqdm import tqdm
import pandas as pd
import os.path
from datetime import datetime

class DataHandler(object):
    def __init__(self, token, datapath=''):
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
                   'start_date' : activity.start_date.strftime('%Y-%m-%d %H:%M:%S')
                   }
        return datarow
    def sync(self):
        if os.path.isfile(self.__datapath):
            df = pd.read_excel(self.__datapath)
            self.__update(df)
        else:
            self.full_sync()
    def __update(self, df):
        i=0
        latest = pd.to_datetime(df['start_date']).max()
        activities = self.__api.get_activities(after=latest)
        for i, activity in enumerate(activities):
            entry = self.__handleActivity(activity)
            df = df.append(entry, ignore_index=True)
        print('Updated datafile with %i new activities' %(i+1))
        df.to_excel(r'data\activities.xlsx')

    def full_sync(self):
        df = pd.DataFrame()
        activities = self.__api.get_activities(limit=8)
        for activity in activities:
            entry = self.__handleActivity(activity)
            df = df.append(entry, ignore_index=True)
        # reverse index so latest has highest number
        df.index = reversed(range(len(df)))
        #flip list so lastest is on the bottom
        df = df.iloc[::-1]
        df.to_excel(r'data\activities.xlsx')

# This code wil be removed, now for testing the object

with open(r'tokens\user_access.token', 'r') as file:
    user_token = file.read()
data = DataHandler(user_token,  r'data\activities.xlsx')
data.sync()


