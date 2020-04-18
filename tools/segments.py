import os.path
import pandas as pd
import time
from stravalib import Client


class SegmentsHandler(object):
    def __init__(self, token, datafolder='data'):
        self.__token = token
        self.__datafolder = datafolder
        self.__ApiLimitCounter = 20
        self.__segmentsfile = os.path.join(self.__datafolder, 'segments.xlsx')
        self.__segmentIDs = pd.DataFrame()
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

    def __handleSegment(self, segmenteffort):
        datarow = {'id': int(segmenteffort.segment.id),
                   'name': str(segmenteffort.name),
                   'distance': float(segmenteffort.distance.num),
                   'activity_type': str(segmenteffort.segment.activity_type),
                   'average_grade': float(segmenteffort.segment.average_grade),
                   'efforts': int(segmenteffort.segment.leaderboard.effort_count),
                   'KOM_time': segmenteffort.segment.leaderboard.entries[1].elapsed_time
                   # 'avg_HR': float(segmenteffort.average_heartrate),
                   # 'avg_Watts': float(segmenteffort.average_watts)
                   }

        for i in reversed(range(len(segmenteffort.segment.leaderboard.entries))):
            if str(segmenteffort.segment.leaderboard.entries[i].athlete_name) == 'Bouke S.':
                datarow['rank'] = segmenteffort.segment.leaderboard.entries[i].rank
                datarow['elapsed_time'] = segmenteffort.segment.leaderboard.entries[i].elapsed_time
                datarow['pr_date'] = segmenteffort.segment.leaderboard.entries[i].start_date_local

        return datarow

    def __getActivities(self):
        df = pd.DataFrame()
        activities = self.__api.get_activities()
        for i, activity in enumerate(activities):
            entry = {'id': int(activity.id)}
            df = df.append(entry, ignore_index=True)
        return df

    def __getSegments(self, last_act):
        df = pd.DataFrame()
        for i in range(len(last_act.segment_efforts)):
            if (last_act.segment_efforts[i].segment.hazardous == 0 and (last_act.segment_efforts[i].segment.id) not in (
                    self.__segmentIDs.values)):  # Only for segments with a leaderboard and unique segments
                entry = self.__handleSegment(last_act.segment_efforts[i])
                df = df.append(entry, ignore_index=True)
                self.__ApiLimitCounter += 1  # Add one for each unique segment
                if self.__ApiLimitCounter > 590:
                    self.__waitAPIlimits()
        return df

    def __setdatatypes(self, df):
        df['pr_date'] = pd.to_datetime(df['pr_date'])
        df['elapsed_time'] = pd.to_timedelta(df['elapsed_time']) * 24 * 60 # Convert to minutes
        df['KOM_time'] = pd.to_timedelta(df['KOM_time']) * 24 * 60  # Convert to minutes
        return df

    def __savefile(self, df):
        df.to_excel(self.__segmentsfile)

    def sync(self, force=False):
        if os.path.isfile(self.__segmentsfile) and not force:
            self.__update()
        else:
            self.full_sync()

    def __update(self):
        print('*UPDATE SEGMENT LIST*')
        print('To be coded.')

    def full_sync(self):
        df = pd.DataFrame()
        print('**FULL SYNC SEGMENT LIST**')
        activities = self.__getActivities()
        for i in range(len(activities)):
            last_act = self.__api.get_activity(activity_id=activities.id[i], include_all_efforts=True)
            entry = self.__getSegments(last_act)
            df = df.append(entry, ignore_index=True)
            self.__segmentIDs = df.id
            self.__ApiLimitCounter += 1  # add one for each activity
            if self.__ApiLimitCounter > 595:
                self.__waitAPIlimits()
        df = self.__setdatatypes(df)
        self.__savefile(df)

    def get_data(self):
        df = pd.read_excel(self.__segmentsfile)
        return self.__setdatatypes(df)
