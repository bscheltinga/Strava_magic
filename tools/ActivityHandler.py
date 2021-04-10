import os.path
import pandas as pd
import time
from stravalib import Client
import numpy as np
import tools.act_features as feat

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
        print('Waiting for STRAVA API limits...')
        while LimitFlag == 1:
            time.sleep(15)  # Wait 15 seconds
            checktime = time.localtime()
            if checktime.tm_min % 15 == 0:
                print('Continuing syncing')
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
            if (entry['has_heartrate'] == True or entry['type'] == 'Run'):
                df = df.append(entry, ignore_index=True)
        return df
    
    def __getFeatures(self, df):
        types = ['time', 'velocity_smooth', 'heartrate', 'distance', 'moving']
        
        # Initiate dataframe for features
        df_features = pd.DataFrame()
        
        # Loop and calculate features
        for i in range(len(df)):
            # Both HR and RUN
            if df['type'][i] == 'Run' and df['has_heartrate'][i] == True and df['manual']==False:
                streams = self.__api.get_activity_streams(int(df['id'][i]), types=types)
                self.__ApiLimitCounter += 1  # add one for each activity stream
                streams = feat.correct_hr(streams)
                
                # ADD FEATURES HERE HR AND Distance
                entry = {
                    'trimp_norm_hr': float(feat.trimp_norm_hr(streams)),
                    'std_hr': float(feat.trimp_norm_hr(streams)),
                    'edwards_trimp': float(feat.edwards_trimp(streams)),
                    'lucia_trimp': float(feat.lucia_trimp(streams)),
                    'banister_trimp': float((df['moving_time'][i] / np.timedelta64(1, 'h')) * df['average_heartrate'][i]),
                    'trimp_norm_distance': float(feat.trimp_norm_distance(streams)),
                    'std_speed': float(feat.std_speed(streams)),
                    'dis_speed_high': float(feat.dis_speed(streams, mode='high')),
                    'dis_speed_low': float(feat.dis_speed(streams, mode='low')),
                    'lucia_trimp_speed': float(feat.lucia_trimp_speed(streams))
                    }
                
            if df['type'][i] != 'Run' and df['has_heartrate'][i] == True and df['manual']==False:
                streams = self.__api.get_activity_streams(int(df['id'][i]), types=types)
                self.__ApiLimitCounter += 1  # add one for each activity stream
                streams = feat.correct_hr(streams)
                
                # Add HR features here
                entry = {
                    'trimp_norm_hr': float(feat.trimp_norm_hr(streams)),
                    'std_hr': float(feat.trimp_norm_hr(streams)),
                    'edwards_trimp': float(feat.edwards_trimp(streams)),
                    'lucia_trimp': float(feat.lucia_trimp(streams)),
                    'banister_trimp': float((df['moving_time'][i] / np.timedelta64(1, 'h')) * df['average_heartrate'][i]),
                    'trimp_norm_distance': np.nan,
                    'std_speed': np.nan,
                    'dis_speed_high': np.nan,
                    'dis_speed_low': np.nan,
                    'lucia_trimp_speed': np.nan
                    }
                
            if df['type'][i] == 'Run' and df['has_heartrate'][i] == False and df['manual']==False:
                streams = self.__api.get_activity_streams(int(df['id'][i]), types=types)
                self.__ApiLimitCounter += 1  # add one for each activity stream
                
                # Add features here
                entry = {
                    'trimp_norm_hr': np.nan,
                    'std_hr': np.nan,
                    'edwards_trimp': np.nan,
                    'lucia_trimp': np.nan,
                    'banister_trimp': np.nan,
                    'trimp_norm_distance': float(feat.trimp_norm_distance(streams)),
                    'std_speed': float(feat.std_speed(streams)),
                    'dis_speed_high': float(feat.dis_speed(streams, mode='high')),
                    'dis_speed_low': float(feat.dis_speed(streams, mode='low')),
                    'lucia_trimp_speed': float(feat.lucia_trimp_speed(streams))
                    }
                
                if df['type'][i] == 'Run' and df['manual'] == True:
                
                    # No streams are available here. So create them by assuming constant speed
                    class Object(object):
                        pass
                    streams = {}
                    streams['velocity_smooth'] = Object()
                    streams['velocity_smooth'].data = [df['average_speed'][i],df['average_speed'][i]]
                
                # Add features here
                entry = {
                    'trimp_norm_hr': np.nan,
                    'std_hr': np.nan,
                    'edwards_trimp': np.nan,
                    'lucia_trimp': np.nan,
                    'banister_trimp': np.nan,
                    'trimp_norm_distance': df['average_speed'][i],
                    'std_speed': np.nan,
                    'dis_speed_high': float(feat.dis_speed(streams, mode='high')),
                    'dis_speed_low': float(feat.dis_speed(streams, mode='low')),
                    'lucia_trimp_speed': float(feat.lucia_trimp_speed(streams))
                    }   
            
            df_features = df_features.append(entry, ignore_index=True)

            if self.__ApiLimitCounter > 595:
                self.__waitAPIlimits()
                
        df = pd.concat([df, df_features], axis=1)
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
        if len(df_new) > 0:
            df_new = self.__setdatatypes(df_new)
            df_new = self.__getFeatures(df_new)
            print('resulted in datafile with %i new activities' % (len(df_new)))
            df_new.index = reversed(range(len(df_new)))
            df_new = df_new.iloc[::-1]
            df = pd.concat([df_new, df], sort=True)
            self.__savefile(df)
        else:
            print('resulted in datafile with 0 new activities')

    def full_sync(self):
        print('**FULL SYNC ACTIVITY FEATURES LIST**')
        activities = self.__api.get_activities(limit=10)
        df = self.__ActivityHandler(activities)
        df= self.__setdatatypes(df)
        df = self.__getFeatures(df)
        # df = self.__calcTrimps(df)
        print('FULL SYNC CONMPLETED \n resulted in datafile with %i activities' % len(df))
        self.__savefile(df)

    def get_data(self):
        df = pd.read_excel(self.__featuresfile)
        return df
