from stravalib import Client
import pandas as pd
import os.path
from sqlalchemy import create_engine

class DataHandler(object):
    def __init__(self, token, datafolder='data'):
        self.__token = token
        self.__datafolder = datafolder
        self.__activitiesfile = os.path.join(self.__datafolder,'activities.xlsx')
        self.__databaseadress = os.path.join('sqlite:///', self.__datafolder, 'strava.db')

        #Setup folders
        self.__setupfolders()
        #Initialize api client
        self.__connect(token)

    def __connect(self, token):
        self.__api = Client(access_token=token)

    def __setupfolders(self):
        if not os.path.isdir(self.__datafolder):
            os.mkdir(self.__datafolder)

    def __handleActivity(self, activity):
        datarow = {'average_heartrate' : activity.average_heartrate,
                   'max_heartrate' : activity.max_heartrate,
                   'average_speed' : float(activity.average_speed),
                   'comment_count' : int(activity.comment_count),
                   'distance' : float(activity.distance),
                   'elapsed_time' : str(activity.elapsed_time),
                   'flagged' : str(activity.flagged),
                   'manual': str(activity.manual),
                   'has_heartrate' : str(activity.has_heartrate),
                   'id' : int(activity.id),
                   'kudos_count' : int(activity.kudos_count),
                   'max_speed' : float(activity.max_speed),
                   'moving_time' : str(activity.moving_time),
                   'name': str(activity.name),
                   'pr_count' : int(activity.pr_count),
                   'total_photo_count' : int(activity.total_photo_count),
                   'type' : str(activity.type),
                   'start_date' : activity.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                   'athlete_count' : int(activity.athlete_count),
                   'gear_name': str(activity.gear_id),
                   'private' : str(activity.private)
                   }
        return datarow

    def __setdatatypes(self, df):
        # alternative in case of errors df["start_date"] = df["start_date"].astype("datetime64")
        # alternative in case of errors df['moving_time'] = df["start_date"].astype('timedelta64[s]')
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['moving_time'] = pd.to_timedelta(df['moving_time'])
        df['elapsed_time'] = pd.to_timedelta(df['elapsed_time'])
        return df

    def __replacegearid(self, df):
        gear_ids = df['gear_name'].unique()
        for id in gear_ids:
            if not id == "None":
                gear_name = self.__api.get_gear(id)
                row_idx = df['gear_name'] == id
                df.loc[row_idx, 'gear_name'] =  gear_name.name
            else:
                row_idx = df['gear_name'] == id
                df.loc[row_idx, 'gear_name'] = "None"
        return df

    def __savefile(self,df):
        df.to_excel(self.__activitiesfile)

    def sync(self, force=False):
        if os.path.isfile(self.__activitiesfile) and not force:
            self.__update()
        else:
            self.full_sync()

    def __update(self):
        print('**UPDATING**')
        i = -1
        df = pd.read_excel(self.__activitiesfile)
        df_new = pd.DataFrame()
        latest = pd.to_datetime(df['start_date']).max()
        activities = self.__api.get_activities(after=latest)
        for i, activity in enumerate(activities):
            entry = self.__handleActivity(activity)
            df_new = df_new.append(entry, ignore_index=True)
        print('resulted in datafile with %i new activities' %(i+1))
        if i+1 >0:
            df_new = self.__replacegearid(df_new)
            df = pd.concat([df,df_new])
            self.__savefile(df)

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
        df = self.__replacegearid(df)
        self.__savefile(df)

    def get_data(self):
        df = pd.read_excel(self.__activitiesfile)
        return self.__setdatatypes(df)

    def setup_sql(self,df):
        engine = create_engine(self.__databaseadress)
        df.to_sql('activities',con=engine, if_exists='replace')
        return engine