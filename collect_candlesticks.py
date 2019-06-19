# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 21:48:10 2019

@author: paveli
"""

import ccxt
import time
from time import gmtime, strftime
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc, candlestick2_ohlc
import pandas as pd
import utils
import config

# Set time frame
# Other possible: '1m', '1h', '1d'
# Check with [exchange.timeframes]
time_frame = '1d'

m1_multy = 60
h1_multy = 3600
d1_multy = 86400

num_fetch_candles_max = 749                                                     # Maximum number of previous candle to fetch (exchange limit)

multy = 60
if(time_frame == '1m'):
    mulgy = m1_multy
if(time_frame == '1h'):
    multy = h1_multy
if(time_frame == '1d'):
    multy = d1_multy


delta_candle = 500

delta_candle = min(delta_candle, num_fetch_candles_max)

bm_begin_day = '2015-09-24 02:00:00'                                            # Fkrst day to consider (exchange dependent)

#bm_end_day = '2019-04-22 02:00:00'                                              # Last day to consider / fixed
bm_end_day = strftime("%Y-%m-%d %H:%M:%S", gmtime())                            # Last day to consider / current time

bm_begin_timestamp = utils.datetime_to_timestamp(bm_begin_day)
bm_end_timestamp = utils.datetime_to_timestamp(bm_end_day)

# Define exchange and connect
bm   = ccxt.bitmex({
    'apiKey': config.apiKey,
    'secret': config.secret,
    })
    
print("Importing ", bm.id)

# Ticker symbol
symbol = 'BTC/USD'
print("Ticker = ", symbol)



#%%


begin = bm_begin_timestamp
dc = delta_candle
ohlcv = []
last_iteration = False
break_loop = False
while True:
    time.sleep(1)                                                               # Hard-coded waiting time to avoid getting banned
    
    begin_dt = utils.add_to_timestamp(time_frame, dc, begin)
    if begin_dt >= bm_end_timestamp:        
        dt = bm_end_timestamp - begin
        dc = int(np.round(dt/(multy*1000)))
        last_iteration = True            
    
    ohlcv_temp = bm.fetch_ohlcv(symbol, timeframe = time_frame, limit = dc, since = begin)
    ohlcv.append(ohlcv_temp)
    
    j = len(ohlcv_temp)
    last_stamp = ohlcv_temp[j-1][0]
    
    if last_iteration:
        begin = bm_end_timestamp
        break_loop = True
    else:
        begin = last_stamp
        
    if break_loop:
        break
    
#%%

ohlcv_all = []
for i in ohlcv:
    for j in i[:-1]:
        ohlcv_all.append(j)
        
ohlcv_array = np.asarray(ohlcv_all)
        
#%%
        
np.savetxt("ohlcv_"+time_frame+".csv", ohlcv_array, delimiter=",")   

    
    