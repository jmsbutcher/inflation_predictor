#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:40:02 2020

@author: JamesButcher
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

econ_data = {}

def access_webpage(url):
    # Access webpage using "requests" library
    #   and get ready to scrape data using "BeautifulSoup" library
    response = requests.get(url)
    s = BeautifulSoup(response.text, 'html.parser')
    return s
        
def get_stlouisfed_data(url):
    soup = access_webpage(url)
    # Extract data value from webpage
    data = soup.find(class_='series-meta-observation-value').get_text()
    # Process string into integer, e.g.: '12,400,000.0000'  -->  12400000
    data = int(data.replace(',', '').split('.')[0])
    return data

econ_data["Money supply - M3"] = \
    get_stlouisfed_data("https://fred.stlouisfed.org/series/MABMM301USM189S")
econ_data["Monetary base - Currency in Circulation"] = \
    get_stlouisfed_data("https://fred.stlouisfed.org/series/MBCURRCIR")
econ_data["Consumer price index"] = \
    get_stlouisfed_data("https://fred.stlouisfed.org/series/CPIAUCSL")

print(econ_data)


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
    
    return data

    








