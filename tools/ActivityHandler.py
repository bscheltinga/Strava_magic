import os.path
import pandas as pd
import time
from stravalib import Client
import numpy as np

class ActivityHandler(object):
    def __init__(self, token, datafolder='data'):
        self.__token = token
        self.__datafolder = datafolder
        self.__ApiLimitCounter = 20
        self.__featuresfile = os.path.join(self.__datafolder, 'activity_features.xlsx')
        # Setup folders
        self.__setupfolders()
        # Initialize api client
        self.__connect(token)

    def __connect(self, token):
        self.__api = Client(access_token=token)

    def __setupfolders(self):
        if not os.path.isdir(self.__datafolder):
            os.mkdir(self.__datafolder)

    def __waitAPIlimits(self):
        LimitFlag = 1
        self.__ApiLimitCounter = 0
        print('Waiting for STRAVA API limits.')
        while LimitFlag == 1:
            time.sleep(15)  # Wait 15 seconds
            checktime = time.localtime()
            if checktime.tm_min % 15 == 0:
                LimitFlag = 0

    def __ActivityHandler(self,activities):
        df = pd.DataFrame()
        for i, activity in enumerate(activities):
            entry = {
                    'id': int(activity.id),
                    'name': str(activity.name),
                    'type': str(activity.type),
                    'start_date': activity.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'moving_time': str(activity.moving_time),
                    'elapsed_time': str(activity.elapsed_time),
                    'distance': float(activity.distance),
                    'average_speed': float(activity.average_speed),
                    'average_heartrate': activity.average_heartrate,
                    'max_heartrate': activity.max_heartrate,
                    'has_heartrate': bool(activity.has_heartrate),
                    'manual': bool(activity.manual)
                     }
            if entry['manual'] == False:
                df = df.append(entry, ignore_index=True)
        return df
    
    def __calcFeatures(self, df):
        types = ['time', 'velocity_smooth', 'heartrate', 'distance', 'moving']
        df['norm_hr'] = np.NaN
        for i in range(len(df)):
            # Both HR and RUN
            if df['type'][i] == 'Run' and df['has_heartrate'][i] == True:
                streams = self.__api.get_activity_streams(int(df['id'][i]), types=types, resolution='medium')
                
                df['norm_hr'][i] = np.mean(np.power(streams['heartrate'].data,4))**(1/4)

            if df['type'][i] != 'Run' and df['has_heartrate'][i] == True:
                streams = self.__api.get_activity_streams(int(df['id'][i]), types=types, resolution='medium')
                
                df['norm_hr'][i] = np.mean(np.power(streams['heartrate'].data,4))**(1/4)
                
#            if df['type'][i] == 'Run' and df['has_heartrate'][i] == False:

#            else:
#                entry = {'Normalized_hr': np.NaN
#                        }
        return df
                
      
    def __savefile(self, df):
        df.to_excel(self.__featuresfile)
        

    def sync(self, force=False):
        if os.path.isfile(self.__featuresfile) and not force:
            self.__update()
        else:
            self.full_sync()

    def __update(self):
        print('*UPDATE ACTIVITY FEATURES LIST*')
        i = -1
        df = pd.read_excel(self.__activitiesfile)
        df_new = pd.DataFrame()
        latest = pd.to_datetime(df['start_date']).max()
        activities = self.__api.get_activities(after=latest)
        for i, activity in enumerate(activities):
            entry = self.__handleActivity(activity)
            df_new = df_new.append(entry, ignore_index=True)
        print('resulted in datafile with %i new activities' % (i + 1))
        if i + 1 > 0:
            df_new = self.__replacegearid(df_new)
            df = pd.concat([df, df_new])
            self.__savefile(df)

    def full_sync(self):
        print('**FULL SYNC ACTIVITY FEATURES LIST**')
        activities = self.__api.get_activities(limit=10)
        df = self.__ActivityHandler(activities)
        df = self.__calcFeatures(df)

        self.__ApiLimitCounter += 1  # add one for each activity or stream???
        if self.__ApiLimitCounter > 595:
            self.__waitAPIlimits()
        self.__savefile(df)

    def get_data(self):
        df = pd.read_excel(self.__featuresfile)
        return self.__setdatatypes(df)
