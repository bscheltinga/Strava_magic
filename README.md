# Strava Magic
Pull your data from Strava and be in control of your own data! The repository is 100% python based and uses the [stravalib](<https://pythonhosted.org/stravalib/>)

**Currently, this script let you**
- save all activities with aggregated data in activities.xlsx,
- save all training load features of rides **with HR** and **all runs** in activity_features.xlsx,
- create a .KML map of all activities with GPS data,
- calculate statistics and totals.

**In the future, this script will**
- apply models on the training load metrics like the [acute:chronic workload ratio](https://www.scienceforsport.com/acutechronic-workload-ratio/),
- apply more statistics
- create the .KML map more efficiently.

## Requirements:
- stravalib
- pprint
- simplekml
- numpy
- time
- matplotlib

Install libraries with:
`pip install -r requirements.txt`

## Authors
- [bscheltinga](https://github.com/bscheltinga)
- [daangeijs](https://github.com/daangeijs)
