import re

import numpy as np


def year(df, range=''):
    year_list = []
    df.index = df['start_date']
    if not range:
        years = np.unique(df['start_date'].values.astype('datetime64[Y]'))
    else:
        years = range
    for year in years:
        df_year = df.loc[df.index.year == int(str(year))]
        year_list.append(df_year)
    year_headers = [re.findall('\d+', s) for s in str(years).split()]
    year_headers = [subitem for item in year_headers for subitem in item]
    return year_list, year_headers


def sport(df, sports=''):
    sport_list = []
    if not sports:
        types = np.unique(df['type'])
    else:
        types = sports
    for sport in types:
        df_sport = df.loc[df['type'] == sport]
        sport_list.append(df_sport)
    return sport_list, types


def gear(df, gear_name=''):
    gear_list = []
    if not gear_name:
        gear = np.unique(df['gear_name'])
    else:
        gear = gear_name
    for name in gear:
        df_sport = df.loc[df['gear_name'] == name]
        gear_list.append(df_sport)
    return gear_list, gear
