from stravalib import Client
import pandas as pd
import os.path

class DataHandler(object):
    def __init__(self, token, datafolder='data'):
        self.__token = token
        self.__datafolder = datafolder
        self.__activitiesfile = os.path.join(self.__datafolder,'activities.xlsx')
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
        if not os.path.isdir(self.__datafolder):
            os.mkdir(self.__datafolder)
        if os.path.isfile(self.__activitiesfile):
            df = self.get_data()
            self.__update(df)
        else:
            self.full_sync()
    def __update(self, df):
        print('**UPDATING**')
        i = -1
        latest = pd.to_datetime(df['start_date']).max()
        activities = self.__api.get_activities(after=latest)
        for i, activity in enumerate(activities):
            entry = self.__handleActivity(activity)
            df = df.append(entry, ignore_index=True)
        print('resulted in datafile with %i new activities' %(i+1))
        df.to_excel(self.__activitiesfile)

    def full_sync(self):
        print('**FULL SYNC**')
        i = -1
        df = pd.DataFrame()
        activities = self.__api.get_activities()
        for i, activity in enumerate(activities):
            entry = self.__handleActivity(activity)
            df = df.append(entry, ignore_index=True)
        # reverse index so latest has highest number
        df.index = reversed(range(len(df)))
        #flip list so lastest is on the bottom
        df = df.iloc[::-1]
        print('resulted in datafile with %i activities' % (i + 1))
        df.to_excel(self.__activitiesfile)

    def get_data(self):
        df = pd.read_excel(self.__activitiesfile)
        return(df)