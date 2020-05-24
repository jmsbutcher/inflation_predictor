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
                "Monetary Base": "https://fred.stlouisfed.org/data/BOGMBASE.txt",
                
                }

econ_data = {}




def access_webpage(url):
    # Access webpage using "requests" library
    #   and get ready to scrape data using "BeautifulSoup" library
    response = requests.get(url)
    s = BeautifulSoup(response.text, 'html.parser')
    return s
        


def obtain_econ_data(date):
    """ Get all economic data points for the date provided.
         - Return a dictionary of { "data name"(string) : data point(float) }
        
        Example: { "CPI" : 256.389 
                   "GDP" : -4.8
                         .
                         .
                                 }
    """
    for key, url in econ_sources.items():
        econ_data[key] = get_stlouisfed_data(url, date)
        
    for key, number in econ_data.items():
        print(key, " --- ", number)
        
    return econ_data



def convert_price_data_to_training_set(item):
    """ Load the price data of item and add all other feature data to it
        to create training examples for machine learning algorithm.
        Example: 
            
            (2-10-20, 1.99)             (2-10-20, 1.99, 2400000, 49.9, ... )
            (2-28-20, 1.99)     --->    (2-28-20, 1.99, 2830000, 42.9, ... )   
            (3-12-20, 2.29)             (3-12-20, 2.29, 3400000, 37.3, ... )
    
    """
    data = pd.DataFrame()
    
    data["Date"] = [entry[0] for entry in item.price_data]
    data["Price"] = [entry[1] for entry in item.price_data]
    

    for key in econ_sources.keys():
        data[key] = list(obtain_econ_data().values())
    
    return data

    



#def get_stlouisfed_data(url):
#    # Get most recently released data point from chart page
#    
#    soup = access_webpage(url)
#    # Extract data value from webpage
#    data = soup.find(class_='series-meta-observation-value').get_text()
#    # Process string into integer, e.g.: '12,400,000.0000'  -->  12400000
#    data = int(data.replace(',', '').split('.')[0])
#    return data
#
#econ_data["Money supply - M3"] = \
#    get_stlouisfed_data("https://fred.stlouisfed.org/series/MABMM301USM189S")
#econ_data["Monetary base - Currency in Circulation"] = \
#    get_stlouisfed_data("https://fred.stlouisfed.org/series/MBCURRCIR")
#econ_data["Consumer price index"] = \
#    get_stlouisfed_data("https://fred.stlouisfed.org/series/CPIAUCSL")
#
#print(econ_data)


def get_stlouisfed_data(url, d):
    """ Get the data point from the St. Louis Fed website specified
        by <url>, for the specified date <d>
        
        Example:    url = https://fred.stlouisfed.org/data/A191RL1Q225SBEA.txt
                    d = datetime.date(2019, 5, 23)
                    
                            .
                            .
                            .
                    2018-10-01   1.1
                    2019-01-01   3.1
                    2019-04-01   2.0    <--- matching data point for 2019-5-23
                    2019-07-01   2.1
                    2019-10-01   2.1
                            .
                            .
                            .
                            
                 >   return 2.0 (type float)
    """
    soup = str(access_webpage(url))
    
    # Find data line corresponding to the given date
    start = soup.rfind(str(d))

    # If date not found, try changing the day to the 1st of the month
    if start == -1:
        d = date(d.year, d.month, 1)
        start = soup.rfind(str(d))
        
    # If date still not found, try subtracting the month, then the year
    break_loop = 100
    while start == -1 and break_loop > 0:
        break_loop -= 1
        if d.month > 1:
            d = date(d.year, d.month-1, 1)
        else:
            d = date(d.year - 1, 12, 1)
        start = soup.rfind(str(d))
    
    end = soup.find("\n", start)
    line = soup[start:end]
    
    data_point = float(line.split(" ")[-1])

    return data_point




#print(get_stlouisfed_data("https://fred.stlouisfed.org/data/A191RL1Q225SBEA.txt", date(2019, 5, 23)))

obtain_econ_data(date.today())

