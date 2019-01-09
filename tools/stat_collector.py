import tools.analytics as anal

def collect(df):
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
    anal.trindex(df)
    # Calculate average speed
    print('=====Average speed=====')
    avg_speed_bike = anal.avg_speed(df.loc[df['type'] == 'Ride'])
    avg_speed_run = anal.avg_speed(df.loc[df['type'] == 'Run'])
    print("Average speed bike: %.2f km/h" % avg_speed_bike)
    print("Average speed run: %.2f km/h" % avg_speed_run)
    # Hot hours
    print('=====Hot hours=====')
    anal.hothours(df)
