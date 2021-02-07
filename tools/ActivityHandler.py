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
                
    def __setdatatypes(self, df):
        # alternative in case of errors df["start_date"] = df["start_date"].astype("datetime64")
        # alternative in case of errors df['moving_time'] = df["start_date"].astype('timedelta64[s]')
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['moving_time'] = pd.to_timedelta(df['moving_time'])
        df['elapsed_time'] = pd.to_timedelta(df['elapsed_time'])
        return df

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
        
        # Initiate features
        df['norm_hr'] = np.NaN
        df['norm_speed'] = np.NaN
        
        # Loop and calculate features
        for i in range(len(df)):
            # Both HR and RUN
            if df['type'][i] == 'Run' and df['has_heartrate'][i] == True:
                streams = self.__api.get_activity_streams(int(df['id'][i]), types=types, resolution='medium')
                
                # ADD FEATURES HERE
                df['norm_hr'][i] = np.mean(np.power(streams['heartrate'].data,4))**(1/4)
                df['norm_speed'][i] = np.mean(np.power(streams['velocity_smooth'].data,4))**(1/4)

            if df['type'][i] != 'Run' and df['has_heartrate'][i] == True:
                streams = self.__api.get_activity_streams(int(df['id'][i]), types=types, resolution='medium')
                
                df['norm_hr'][i] = np.mean(np.power(streams['heartrate'].data,4))**(1/4)
                
            if df['type'][i] == 'Run' and df['has_heartrate'][i] == False:
                streams = self.__api.get_activity_streams(int(df['id'][i]), types=types, resolution='medium')
                
                df['norm_speed'][i] = np.mean(np.power(streams['velocity_smooth'].data,4))**(1/4)

            self.__ApiLimitCounter += 1  # add one for each activity
            if self.__ApiLimitCounter > 595:
                self.__waitAPIlimits()
        return df
                
      
    def __savefile(self, df):
        df.to_excel(self.__featuresfile, index=False)
        

    def sync(self, force=False):
        if os.path.isfile(self.__featuresfile) and not force:
            self.__update()
        else:
            self.full_sync()

    def __update(self):
        print('*UPDATE ACTIVITY FEATURES LIST*')
        df = pd.read_excel(self.__featuresfile)
        latest = pd.to_datetime(df['start_date']).max()
        activities = self.__api.get_activities(after=latest)
        df_new = self.__ActivityHandler(activities)
        df_new = self.__calcFeatures(df_new)
        print('resulted in datafile with %i new activities' % (len(df_new)))
        if len(df_new) > 0:
            df_new.index = reversed(range(len(df_new)))
            df_new = df_new.iloc[::-1]
            df = pd.concat([df_new, df], sort=True)
            self.__savefile(df)

    def full_sync(self):
        print('**FULL SYNC ACTIVITY FEATURES LIST**')
        activities = self.__api.get_activities()
        df = self.__ActivityHandler(activities)
        df = self.__calcFeatures(df)
        print('resulted in datafile with %i activities' % len(df))
        self.__savefile(df)

    def get_data(self):
        df = pd.read_excel(self.__featuresfile)
        return self.__setdatatypes(df)
