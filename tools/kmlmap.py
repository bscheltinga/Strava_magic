from stravalib import Client
import numpy as np
import simplekml

def create_kml(usertoken, df):
    client = Client(access_token=usertoken)

    # Initiate KML
    kml = simplekml.Kml()


    for idx, row in df.iterrows():
        # if x % 500 == 0 and x > 1:  # To prevent exceeding strava limits
        #     print('Waiting for STRAVA API limits. Get a coffee!')
        #     print(time.localtime())
        #     time.sleep(900)
        id = row['id']
        types = ['latlng']
        print(idx)
        streams = client.get_activity_streams(id, types=types, resolution='medium')
        if [True for x in streams.keys() if x == 'latlng']: #check if latlng data is available as datastream
            cords = np.array(streams['latlng'].data)
            cords = np.flip(cords, axis=1)  # Flip the cords for right kml notation
            ls = kml.newlinestring(name=row['name'], coords=cords, extrude=1)
    kml.save("KMLmap.kml")