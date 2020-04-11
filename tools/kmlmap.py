from stravalib import Client
import numpy as np
import simplekml
import time
from tqdm import tqdm
def create_kml(usertoken, df):
    client = Client(access_token=usertoken)
    # Initiate KML
    kml = simplekml.Kml()
    # Get gps data from every activity
    for idx, row in tqdm(df.iterrows(), total=df.shape[0],desc='Creating KML file' ):
        if idx % 500 == 0 and idx > 1:  # To prevent exceeding strava limits
            print('Waiting for STRAVA API limits.')
            time.sleep(900)
        id = row['id']
        types = ['latlng']
        streams = client.get_activity_streams(id, types=types, resolution='medium')
        if [True for x in streams.keys() if x == 'latlng']: # Check if latlng data is available as datastream
            cords = np.array(streams['latlng'].data)
            cords = np.fliplr(cords)  # Flip the cords for right kml notation
            kml.newlinestring(name=row['name'], coords=cords, extrude=1)
    kml.save(r"data/KMLmap.kml")