import tools.analytics as anal
import pandas as pd

def collect(df_list, headers):
    total = pd.DataFrame()
    for df in df_list:
        print('=====Totals=====')
        totals = anal.totals(df)
        time = str(totals['elapsed_time'])
        print('totals: distance={:.2f}, kudos={}, avg_kudos={:.2f}, elapsed time={}'.format(totals['distance'],
                                                                                             totals['kudos'],
                                                                                             totals['avg_kudos'], time))
        # Show h-index of dataset
        print('=====H-Index=====')
        h = anal.h_index(df)
        print("H-index overall: %i" % h)
        trindex = anal.trindex(df)
        # Calculate average speed
        print('=====Average speed=====')
        avg_speed = anal.avg_speed(df)
        # Hot hours
        print('=====Hot hours=====')
        if len(df) > 3:
            hothours = anal.hothours(df)
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
    parsed_df.to_excel(r'data\\'+output_name)
    print("Save to 'data\\'"+str(output_name))