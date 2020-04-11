import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timezone
import collections

def h_index(df, figures=False):
    # Sum activities per day
    df.index = df['start_date']
    df = df.resample('D').sum()
    df = df.drop(df.loc[df['distance'] == 0].index)

    H_index = 0
    H_index_distance = np.array(df['distance'].tolist())/1000
    # Determine the H-index
    H_index_distance = sorted(H_index_distance, reverse=True)
    for i in range(len(H_index_distance)):
        if i > H_index_distance[i]:
            H_index = i-1  # Outputs the H_index
            break
    if figures:
        plt.figure()
        plt.hist(H_index_distance)  # Tweak these parameters
        plt.xlabel('Kilometers')
        plt.ylabel('Activity count')
        plt.title('Histogram of activities')

        # Calculate the amount of activities for each bin
        H_index_cum = []
        for i in range(int(max(H_index_distance))):
            H_index_cum.append(sum(j > (i + 1) for j in H_index_distance))

        plt.figure()
        plt.bar(np.add(list(range(0, int(max(H_index_distance)))),1),H_index_cum)
        plt.plot([0, max(H_index_distance)], [0, max(H_index_distance)],'r')  # Add the H-Index line
        plt.xlabel('Kilometers')
        plt.ylabel('Activity count')
        plt.title('Cumulative histogram')
        # Show plots
        plt.show()

    return H_index

def totals(df):
    distance = df['distance'].sum()/1000
    elapsed_time = df['elapsed_time'].sum()
    moving_time = df['moving_time'].sum()
    kudos = df['kudos_count'].sum()
    avg_kudos = df['kudos_count'].mean() # Here devided by the amount of not private activities.
    output = {'distance' : distance,
              'elapsed_time' : elapsed_time,
              'kudos' : kudos,
              'moving_time' : moving_time,
              'avg_kudos' : avg_kudos}

    return output

def hr_vs_speed(df):
    df = df.loc[df['has_heartrate'] == True]
    speed = np.array(df['average_speed'].tolist())*3.6
    hr = df['average_heartrate'].tolist()
    plt.plot(speed,hr,'r*')
    plt.title('Heart rate vs Speed plot')
    plt.xlabel('Speed [km/h]')
    plt.ylabel('Heart rate [bpm]')
    plt.show()

def hothours(df, figures=False):
    hours =[]
    for id, item in enumerate(df["start_date"]):
        local_time = item.replace(tzinfo=timezone.utc).astimezone(tz='Europe/Amsterdam')
        hours.append(local_time.hour)
    counts, range = np.histogram(hours, bins=np.max(hours)-np.min(hours))
    sort = np.argsort(counts)[::-1]
    morning = counts[range[:-1] < 12].sum() / counts.sum()
    noon = counts[(range[:-1] >= 12) & (range[:-1] < 18)].sum() /counts.sum()
    evening = counts[range[:-1] >= 18].sum() /counts.sum()
    print('Ratio morning/noon/evening: {:.2f}/{:.2f}/{:.2f}'.format(morning,noon,evening))
    top = sort[0:3]
    print('Hot hours: {}'.format(range[top]))
    if figures:
        plt.bar(counts, bins=range)
        plt.xticks(range)
        plt.show()
    return {'ratio' : '{:.2f}/{:.2f}/{:.2f}'.format(morning,noon,evening), 'hothours' : range[top]}

def trindex(df):
    # Calculate tri H-index, a.k.a. H-Trindex
    df = df.loc[(df['type'] == 'Ride') | (df['type'] == 'Run') | (df['type'] == 'Swim')]
    df.index = df['start_date']
    df = df.resample('D').sum()
    df = df.drop(df.loc[df['distance'] == 0].index)
    df['start_date'] = df.index
    h_sport = h_index(df, figures=False)
    print('H-Trindex: %i' % (h_sport))
    return h_sport
def word_usage(df):
    words = []
    for i in range(len(df)):
        words = words + df['name'][i].split()
    top_words = collections.Counter(map(str.lower, words)).most_common(20)
    print(top_words)
    return top_words

def avg_speed(df):
    # Calculate
    mean_time = (df['moving_time'] / np.timedelta64(1, 's')).mean()
    avg_speed = (df['distance'].mean()/ mean_time)*3.6
    return avg_speed