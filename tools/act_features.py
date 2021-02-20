# -*- coding: utf-8 -*-
import numpy as np
'''
To include: speed threshold (distance above and below certain speed)
Lucia, Edwards, Banister trimps (werk Casteele, Gosseries)  #TODO
'''

# Heart rate features
def norm_hr(streams):
    power = 4
    # Convert to int64 for ^4 calculation
    hr = [np.int64(i) for i in streams['heartrate'].data[:-1]]
    hr_power = sum((np.diff(streams['time'].data) * np.power(hr,power) *
               streams['moving'].data[:-1]))
    time = sum(np.diff(streams['time'].data) * streams['moving'].data[:-1])   
    norm_hr = (hr_power/time)**(1/power)
    
    return norm_hr

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
    
def norm_speed(streams):
    power = 4
    # Convert to int64 for ^4 calculation
    speed_power = sum((np.diff(streams['time'].data) * np.power(streams['velocity_smooth'].data[:-1],power) *
               streams['moving'].data[:-1]))
    time = sum(np.diff(streams['time'].data) * streams['moving'].data[:-1])   
    norm_speed = (speed_power/time)**(1/power)
    
    return norm_speed


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

def dis_speed(streams,threshold=12, mode='high'):
    '''
    Calculate the distance covered above and below the set threshold
    with mode: high or low. With high above the threshold and low below.
    '''
    threshold = threshold/3.6
    if mode == 'low':
        values = np.array([0 if i > threshold else i for i in streams['velocity_smooth'].data])
    if mode == 'high':
        values = np.array([0 if i <= threshold else i for i in streams['velocity_smooth'].data])
    
    dis_speed = np.sum(values[:-1]*np.diff(streams['time'].data))
    return dis_speed

def correct_hr(streams):
    '''
    Replace values >205 for the mean value
    '''
    threshold = 205
    # Remove values above threshold and replace for np.nan
    streams['heartrate'].data = [np.nan if i >=threshold else i for i in streams['heartrate'].data]
    mean = np.nanmean(streams['heartrate'].data)
    # Replace nans for mean value.
    streams['heartrate'].data = [mean if np.isnan(i) == True else i for i in streams['heartrate'].data]
    return streams