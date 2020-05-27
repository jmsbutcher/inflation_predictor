#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:40:02 2020

@author: JamesButcher
"""
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
        

def convert_price_data_to_training_set(item):
    """ Load the price data of item and add all other feature data to it
        to create training examples for machine learning algorithm.
        Example: 
         item.price_data :        data : <DataFrame>: {
               <List>                    "Date" "Price" "Key1"  "Key2" ...
          [ (2-10-20, 1.99)             (2-10-20, 1.99, 2400000, 49.9, ... )
            (2-28-20, 1.99)     --->    (2-28-20, 1.99, 2830000, 42.9, ... )   
            (3-12-20, 2.29)             (3-12-20, 2.29, 3400000, 37.3, ... )
                  .                                     .
                  .         ]                           .                   }
    """
    data = pd.DataFrame()
    
    dates = [entry[0] for entry in item.price_data]
    data["Date"] = dates
    data["Price"] = [entry[1] for entry in item.price_data]

    econ_data = obtain_econ_data(dates)
        
    for key in econ_sources.keys():
        data[key] = econ_data[key]
        
    print(data)
    
    return data


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

