import tools.statistics as stats
import pandas as pd
import os

def collect(df_list, headers):
    total = pd.DataFrame()
    for df in df_list:
        print('=====Totals=====')
        totals = stats.totals(df)
        time = str(totals['elapsed_time'])
        print('totals: distance={:.2f}, kudos={}, avg_kudos={:.2f}, elapsed time={}'.format(totals['distance'],
                                                                                             totals['kudos'],
                                                                                             totals['avg_kudos'], time))
        # Show h-index of dataset
        print('=====H-Index=====')
        h = stats.h_index(df)
        print("H-index overall: %i" % h)
        trindex = stats.trindex(df)
        # Calculate average speed
        print('=====Average speed=====')
        avg_speed = stats.avg_speed(df)
        # Hot hours
        print('=====Hot hours=====')
        if len(df) > 3:
            hothours = stats.hothours(df)
        else:
            hothours = {'ratio' : 'na', 'hothours' : [0,0,0]}
        output = {'distance' : totals['distance'],
                  'elapsed_time' : str(totals['elapsed_time']),
                  'kudos' : totals['kudos'],
                  'moving_time' : str(totals['moving_time']),
                  'avg_kudos' : totals['avg_kudos'],
                  'hindex' : h,
                  'trindex' : trindex,
                  'avg_speed' : avg_speed,
                  'hothours_ratio' : hothours['ratio'],
                  'hothours' : hothours['hothours']
                }
        total = total.append(output, ignore_index='True')
    total.index = headers
    return total

def output(parsed_df, output_name):
    parsed_df.to_excel(os.path.join('data',output_name))
    print("Saved to "+os.path.join('data',output_name))