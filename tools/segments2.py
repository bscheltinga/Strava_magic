import os.path
import pandas as pd
from stravalib import Client


class SegmentsHandler(object):
    def __init__(self, token, datafolder='data'):
        self.__token = token
        self.__datafolder = datafolder
        self.__ApiLimitCounter = 580
        self.__activitiesfile = os.path.join(self.__datafolder, 'segments.xlsx')

        # Setup folders
        self.__setupfolders()
        # Initialize api client
        self.__connect(token)

    def __connect(self, token):
        self.__api = Client(access_token=token)

    def __setupfolders(self):
        if not os.path.isdir(self.__datafolder):
            os.mkdir(self.__datafolder)

    def __handleActivity(self, activity):
        datarow = {'id': int(activity.id)}
        return datarow

    def __handleSegment(self, segmenteffort):
        datarow = {'id': int(segmenteffort.segment.id),
                 'name': str(segmenteffort.name),
                 'distance': float(segmenteffort.distance.num),
                 'activity_type': str(segmenteffort.segment.activity_type),
                 'average_grade': float(segmenteffort.segment.average_grade),
                 'efforts': int(segmenteffort.segment.leaderboard.effort_count),
                 'KOM_time': segmenteffort.segment.leaderboard.entries[1].elapsed_time
                 }
        return datarow

    def __getActivities(self):
        df = pd.DataFrame()
        activities = self.__api.get_activities()
        for i, activity in enumerate(activities):
            entry = self.__handleActivity(activity)
            df = df.append(entry, ignore_index=True)
        return df

    def __getSegments(self, last_act):
        df = pd.DataFrame()
        for i in range(len(last_act.segment_efforts)):
            if last_act.segment_efforts[i].segment.hazardous == 0: # Only for segments with a leaderboard
                entry = self.__handleSegment(last_act.segment_efforts[i])
                df = df.append(entry, ignore_index=True)
        return df

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
                df.loc[row_idx, 'gear_name'] = gear_name.name
            else:
                row_idx = df['gear_name'] == id
                df.loc[row_idx, 'gear_name'] = "None"
        return df

    def __savefile(self, df):
        __self.test = 10 #Do not save
        # df.to_excel(self.__activitiesfile)

    def sync(self, force=False):
        if os.path.isfile(self.__activitiesfile) and not force:
            self.__update()
        else:
            self.full_sync()

    def __update(self):
        self.__test = 10 # DEbug option

    def full_sync(self):
        df = pd.DataFrame()
        print('**FULL SYNC SEGMENT LIST**')
        activities = self.__getActivities()
        for i in range(len(activities)):
            last_act = self.__api.get_activity(activity_id=activities.id[i], include_all_efforts=True)
            entry = self.__getSegments(last_act)
            df = df.append(entry, ignore_index=True)

        df = self.__replacegearid(df)
        self.__savefile(df)

    def get_data(self):
        df = pd.read_excel(self.__activitiesfile)
        return self.__setdatatypes(df)
