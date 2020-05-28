#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:40:02 2020

@author: JamesButcher
"""
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date

econ_sources = {"CPI": "https://fred.stlouisfed.org/data/CPIAUCNS.txt",
                "GDP": "https://fred.stlouisfed.org/data/A191RL1Q225SBEA.txt",
                "Monetary Base": "https://fred.stlouisfed.org/data/BOGMBASE.txt"
                
                }

econ_data = {}


def access_webpage(url):
    """ Access webpage using "requests" library,
          and get ready to scrape data using "BeautifulSoup"
    """
    response = requests.get(url)
    s = BeautifulSoup(response.text, 'html.parser')
    return s
        

#def convert_price_data_to_training_set(item):
#    """ Load the price data of item and add all other feature data to it
#        to create training examples for machine learning algorithm.
#        Example: 
#         item.price_data :        data : <DataFrame>: {
#               <List>                    "Date" "Price" "Key1"  "Key2" ...
#          [ (2-10-20, 1.99)             (2-10-20, 1.99, 2400000, 49.9, ... )
#            (2-28-20, 1.99)     --->    (2-28-20, 1.99, 2830000, 42.9, ... )   
#            (3-12-20, 2.29)             (3-12-20, 2.29, 3400000, 37.3, ... )
#                  .                                     .
#                  .         ]                           .                   }
#    """
#    data = pd.DataFrame()
#    
#    dates = [entry[0] for entry in item.price_data]
#    data["Date"] = dates
#    data["Price"] = [entry[1] for entry in item.price_data]
#
#    econ_data = obtain_econ_data(dates)
#        
#    for key in econ_sources.keys():
#        data[key] = econ_data[key]
#        
#    print(data)
#    
#    return data


def convert_price_data_to_training_set(item, timeframe):
    """ Load the price data of item and add all other feature data to it
        to create training examples for machine learning algorithm.
        Example: 
            
         item.price_data :        data : 
               <List>                       <DataFrame> 
                                    { "Date" "Price" "Key1"  "Key2" ... "Y"
          [ (2-10-20, 1.99)          (2-10-20, 1.99, 2400000, 49.9, ... 1.99)
            (2-28-20, 1.99)   --->   (2-28-20, 1.99, 2830000, 42.9, ... 2.29)   
            (3-12-20, 2.29)          (3-12-20, 2.29, 3400000, 37.3, ... 2.49)
                  .                                     .
                  .         ]                           .                    }
    """
    data = pd.DataFrame()
    
    # Add Date and Price columns
    dates = [entry[0] for entry in item.price_data]
    data["Date"] = dates
    prices = [entry[1] for entry in item.price_data]
    data["Price"] = prices

    # Add the rest of the feature columns
    econ_data = obtain_econ_data(dates)
    for key in econ_data.keys():
        data[key] = econ_data[key]
        
    # Add the groundtruth (Y-values) column
    data["Y"] = generate_y_values(dates, prices, timeframe)
        
    print(data)
    
    return data


def generate_y_values(dates, prices, timeframe, max_allowed_time_diff = 15):
    """ Generate a list of y-values, consisting of prices for entries that are
        closest to <timeframe> days in the future.
        
        If there are no other entries within the maximum allowed time
        difference minus the timeframe for a given entry, then the y-value
        for that entry is None. Thus it won't be used in the training set.
    """
    y_values = [None] * len(dates)
    length = len(dates)
    
    # Simply use present prices if not trying to predict into the future
    if timeframe == 0:
        return prices

    for entry_num in range(0, length-1):
        print(entry_num)
        print(range(entry_num+1, length))
        # Find index of price entry closest away to future timeframe
        time_diffs = [(dates[future_entry_num] - dates[entry_num]).days for \
                      future_entry_num in range(entry_num+1, length)]
        print("Time diffs before:", time_diffs)
        time_diffs = abs(np.array(time_diffs) - timeframe)
        print("Time diffs after:", time_diffs)
        min_index = entry_num 
        min_diff = time_diffs[0]
        for k in range(1, len(time_diffs)):
            if time_diffs[k] < min_diff:
                min_diff = time_diffs[k]
                min_index = entry_num + k
        # Add the price of that entry at the y-value
        if min_diff < max_allowed_time_diff:
            y_values[entry_num] = prices[min_index + 1]
        
    return y_values


def get_stlouisfed_data(url, dates):
    """ Get the data points from the St. Louis Fed website specified
        by <url>, for the specified dates <dates>
        
        Search backward from the latest data point to the earliest. Find
        the data point from the date most recently before the specified date.
        
        Example:    url = https://fred.stlouisfed.org/data/A191RL1Q225SBEA.txt
                    dates = [2019-2-3, 2019-3-14, 2019-4-22]
                    
                            .
                            .
                            .
                    2018-10-01   1.1
                    2019-01-01   3.1    <--- matching data point for first 2
                    2019-04-01   2.0    <--- matching data point for 2019-4-22
                    2019-07-01   2.1
                    2019-10-01   2.1
                            .
                            .
                            .
                            
                 >   return [3.1, 2.0] 
    """
    data_points = []
    
    soup = str(access_webpage(url))
    
    for d in dates:
        # Find data line corresponding to the given date
        start = soup.rfind(str(d))
    
        # If date not found, try changing the day to the 1st of the month
        if start == -1:
            d = date(d.year, d.month, 1)
            start = soup.rfind(str(d))
            
        # If date still not found, try subtracting the month, then the year,
        #   by 1 until a match is found, or until break loop limit is reached
        break_loop = 1000
        while start == -1 and break_loop > 0:
            break_loop -= 1
            if d.month > 1:
                d = date(d.year, d.month-1, 1)
            else:
                d = date(d.year - 1, 12, 1)
            start = soup.rfind(str(d))
        
        end = soup.find("\n", start)
        line = soup[start:end]
        
        data_points.append(float(line.split(" ")[-1]))

    return data_points


def obtain_econ_data(dates):
    """ Get all economic data points for the list of dates provided.
         - Return a dict of { "econ data point name" : [data points(float)] }
        
        Example: 
                    dates: [2020-2-3, 2020-2-14, 2020-3-22]
            
                 { "CPI" : [256.389,  243.221,   270.238  ]
                   "GDP" : [-4.8,     -4.8,      -4.8     ]
                         .
                         .
                         .                                 }
    """
#    print("Dates: ", [str(d) for d in dates])
    
    for key, url in econ_sources.items():
        econ_data[key] = get_stlouisfed_data(url, dates)
        
#    for key, numbers in econ_data.items():
#        print(key, " --- ", end="")
#        for number in numbers:
#            print(number, end=" ")
#        print()
        
    return econ_data

