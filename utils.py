# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 10:36:31 2018

@author: paveli
"""

import numpy as np
import datetime

time_format = '%Y-%m-%d %H:%M:%S'

###############################################################################
# Simple(linear) moving average
def simple_moving_average(data, window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(data, weigths, 'valid')
    return smas # as a numpy array
    
###############################################################################
# Exponential moving average    
def exponential_moving_average(data, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    weights = weights[::-1]
    emas =  np.convolve(data, weights, mode='full')[:len(data)]
    emas = emas[window-1:len(data)]    
    return emas
    
###############################################################################
# Convert bitmex timestamp to datetime
def timestamp_to_datetime(stamp):
    date_time = datetime.datetime.fromtimestamp(stamp/1000.0).strftime(time_format)
    return date_time
    
###############################################################################
# Convert list of bitmex timestamp to list of datetime
def timestamp_to_datetime_list(stamp):
    date_time = []
    for s in stamp:
        date_time_temp = datetime.datetime.fromtimestamp(s/1000.0).strftime(time_format)
        date_time.append(date_time_temp)
    return date_time
    
###############################################################################
# Convert datetime to bitmex timestamp
def datetime_to_timestamp(date):
    date_obj = datetime.datetime.strptime(date, time_format)
    timestamp = datetime.datetime.timestamp(date_obj)
    return int(timestamp*1000)
    
###############################################################################    
# Convert list of datetime to list of bitmex timestamp
def datetime_to_timestamp_list(date):
    timestamp = []
    for d in date:
        date_obj = datetime.datetime.strptime(d, time_format)
        timestamp_temp = datetime.datetime.timestamp(date_obj)
        timestamp.append(int(timestamp_temp*1000))
    return timestamp
    
###############################################################################   
def add_to_timestamp(kind, amount, stamp):
    date = timestamp_to_datetime(stamp)
    date_obj = datetime.datetime.strptime(date, time_format)  
    if kind == '1m':
        dt = datetime.timedelta(minutes=amount)
        date_obj_new = date_obj + dt
    if kind == '1h':
        dt = datetime.timedelta(hours=amount)
        date_obj_new = date_obj + dt
    if kind == '1d':
        dt = datetime.timedelta(days=amount)     
        date_obj_new = date_obj + dt
    
    stamp_new = int(datetime.datetime.timestamp(date_obj_new)*1000)
    return stamp_new
###############################################################################    
def autocorr1(x):
    result = np.correlate(x, x, mode='full')
    print(result)
    return result[int(result.size/2):]
###############################################################################     
def autocorr2 (x) :
    xp = x-np.mean(x)
    f = np.fft.fft(xp)
    p = np.array([np.real(v)**2+np.imag(v)**2 for v in f])
    pi = np.fft.ifft(p)
    return np.real(pi)[:int(x.size/2)]/np.sum(xp**2)
        







