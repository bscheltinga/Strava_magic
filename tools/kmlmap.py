import time

import numpy as np
import simplekml
from stravalib import Client
from tqdm import tqdm


def create_kml(usertoken, df):
    client = Client(access_token=usertoken)
    # Initiate KML
    kml = simplekml.Kml()
    limit_count = 0
    i_lim = 1
    # Get gps data from every activity
    for a, row in tqdm(df.iterrows(), total=df.shape[0], desc='Creating KML file'):

        limit_count += 1
        if limit_count > (580 * i_lim):  # To prevent exceeding strava limits
            LimitFlag = 1
            i_lim += 1
            print('Waiting for STRAVA API limits.')
            while LimitFlag == 1:
                time.sleep(20)  # Wait 30 seconds
                checktime = time.localtime()
                if checktime.tm_min % 15 == 0:
                    LimitFlag = 0

        id = row['id']
        types = ['latlng']
        streams = client.get_activity_streams(id, types=types, resolution='medium')
        if [True for x in streams.keys() if x == 'latlng']:  # Check if latlng data is available as datastream
            cords = np.array(streams['latlng'].data)
            cords = np.fliplr(cords)  # Flip the cords for right kml notation
            kml.newlinestring(name=row['name'], coords=cords, extrude=1)
    kml.save(r"data/KMLmap_run.kml")
