import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def h_index(df, figures=False):
    # 1-12-2018 Calculate H-index from run and rides.
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
    elapsed_time = pd.to_timedelta(df['elapsed_time']).sum()
    kudos = df['kudos_count'].sum()
    moving_time = pd.to_timedelta(df['moving_time']).sum()
    avg_kudos = df['kudos_count'].mean()
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
    plt.show()

