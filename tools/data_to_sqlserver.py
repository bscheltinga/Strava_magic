# -*- coding: utf-8 -*-

'''
Data science script to push the data from strava magic to the sql server.
Server credentials are found in data\sqldata.txt
'''
from sqlalchemy import create_engine
import pandas as pd

connectsql = open(r'C:\Users\bscheltinga\Documents\Strava_magic\data\sqldata.txt','r')
connectsql = connectsql.read()

dbschema='project' # Searches left-to-right
engine = create_engine(connectsql,
    connect_args={'options': '-csearch_path={}'.format(dbschema)})

df = pd.read_excel(r'C:\Users\bscheltinga\OneDrive - Universiteit Twente\Data Science\Project\Models_table.xlsx')
# Some other example server values are
df.to_sql('Models_table', engine)