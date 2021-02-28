# -*- coding: utf-8 -*-
import numpy as np
'''
To include: speed threshold (distance above and below certain speed)
Lucia, Edwards, Banister trimps (werk Casteele, Gosseries)  #TODO
'''

# Heart rate features
def trimp_norm_hr(streams):
    power = 4
    # Convert to int64 for ^4 calculation
    hr = [np.int64(i) for i in streams['heartrate'].data[:-1]]
    hr_power = sum((np.diff(streams['time'].data) * np.power(hr,power) *
               streams['moving'].data[:-1]))
    time = sum(np.diff(streams['time'].data) * streams['moving'].data[1:])   
    norm_hr = (hr_power/time)**(1/power)
    duration_h = sum(np.array(np.diff(streams['time'].data)) * 
                     np.array(streams['moving'].data[1:]))/3600
    trimp_norm_hr = norm_hr*duration_h
    return trimp_norm_hr

def edwards_trimp(streams, hr_max=200):
    '''
    HR is corrected for zones (50-60%, 60-70%, 70-80%, 80-90% and 90-100% of HRmax)
    Then, the time spend in each zone is multiplied by the zone number.
    '''
    # Calculate zone bottom value
    z1 = 0.5*hr_max
    z2 = 0.6*hr_max
    z3 = 0.7*hr_max
    z4 = 0.8*hr_max
    z5 = 0.9*hr_max
    
    # Calculate HR IF moving
    hr_zones = streams['heartrate'].data*np.array(streams['moving'].data)
    
    # Replace value for the zone
    hr_zones = np.where((hr_zones >= z1) & (hr_zones < z2), 1, hr_zones)
    hr_zones = np.where((hr_zones >= z2) & (hr_zones < z3), 2, hr_zones)
    hr_zones = np.where((hr_zones >= z3) & (hr_zones < z4), 3, hr_zones)
    hr_zones = np.where((hr_zones >= z4) & (hr_zones < z5), 4, hr_zones)
    hr_zones = np.where(hr_zones >= z5, 5, hr_zones)
    
    edwards_trimp = sum(hr_zones[1:]*np.diff(streams['time'].data))/60

    return edwards_trimp

def lucia_trimp(streams, thresholds=[175, 185]):
    '''
    HR is corrected for zones based on VT (<VT= 1, VT-RCP = 2, >RCP = 3))
    Then, the time spend in each zone is multiplied by the zone number.
    '''   
    # Calculate HR IF moving
    hr_zones = streams['heartrate'].data*np.array(streams['moving'].data)
    
    # Replace value for the zone
    hr_zones = np.where(hr_zones < thresholds[0], 1, hr_zones)
    hr_zones = np.where((hr_zones >= thresholds[0]) & (hr_zones < thresholds[1]), 2, hr_zones)
    hr_zones = np.where(hr_zones >= thresholds[1], 3, hr_zones)
    
    edwards_trimp = sum(hr_zones[1:]*np.diff(streams['time'].data))/60

    return lucia_trimp


def std_hr(streams):
    '''
    This is not a very proper technique as steady data is stored at a lower
    sampling frequency. Therefore, this std will result in an over-estimation
    of the true value.
    
    Standard deviation is only calculated for values that are labelled as 
    moving=True.
    '''
    i = np.where(np.array(streams['moving'].data) == True)[0]
    std_hr = np.std(np.array(streams['heartrate'].data)[i])
    
    return std_hr

def hrss(streams):
    hrss = np.NaN
    return hrss

# Velocity features
    
def trimp_norm_distance(streams):
    power = 4
    # Convert to int64 for ^4 calculation
    speed_power = sum((np.diff(streams['time'].data) * np.power(streams['velocity_smooth'].data[:-1],power) *
               streams['moving'].data[1:]))
    time = sum(np.diff(streams['time'].data) * streams['moving'].data[:-1])   
    norm_speed = (speed_power/time)**(1/power)
    duration_h = sum(np.array(np.diff(streams['time'].data)) * 
                     np.array(streams['moving'].data[1:]))/3600
    trimp_norm_distance = norm_speed*duration_h*3600
    
    return trimp_norm_distance


def std_speed(streams):
    '''
    This is not a very proper technique as steady data is stored at a lower
    sampling frequency. Therefore, this std will result in an over-estimation
    of the true value.
    
    Standard deviation is only calculated for values that are labelled as 
    moving=True.
    '''
    i = np.where(np.array(streams['moving'].data) == True)[0]
    std_speed = np.std(np.array(streams['velocity_smooth'].data)[i])
    
    return std_speed

def dis_speed(streams, threshold=12, mode='high'):
    '''
    Calculate the distance (meters) covered above and below the set threshold 
    (km/h) with mode: high or low. With high above the threshold and low below.
    '''
    threshold = threshold/3.6
    if mode == 'low':
        values = np.array([0 if i > threshold else i for i in streams['velocity_smooth'].data])
    if mode == 'high':
        values = np.array([0 if i <= threshold else i for i in streams['velocity_smooth'].data])
    
    dis_speed = np.sum(values[:-1]*np.diff(streams['time'].data))
    return dis_speed

# Data correction functions
    
def correct_hr(streams):
    '''
    Replace values >205 for the mean value. Physiological not possible for me
    '''
    threshold = 205
    # Remove values above threshold and replace for np.nan
    streams['heartrate'].data = [np.nan if i >=threshold else i for i in streams['heartrate'].data]
    mean = np.nanmean(streams['heartrate'].data)
    # Replace nans for mean value.
    streams['heartrate'].data = [mean if np.isnan(i) == True else i for i in streams['heartrate'].data]
    return streams