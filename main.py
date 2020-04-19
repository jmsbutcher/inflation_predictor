#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:22:44 2020

@author: JamesButcher
"""


import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot


price_data = {}
econ_data = {}


def access_webpage(url):
    # Access webpage using "requests" library
    #   and get ready to scrape data using "BeautifulSoup" library
    response = requests.get(url)
    s = BeautifulSoup(response.text, 'html.parser')
    return s
    
def add_item(item_name):
    n = len(econ_data)
    econ_data_columns = list(econ_data.keys())
    columns = 
    price_data[item_name] = pd.DataFrame(columns=)
        
def add_data_entry(item_name, date, price):
    """
    Add the price of the item, today's date, and today's associated 
    economic data into the item's data list.
    """
    
    price_data[item_name].add_row
    
        
def get_stlouisfed_data(url):
    soup = access_webpage(url)
    # Extract data value from webpage
    data = soup.find(class_='series-meta-observation-value').get_text()
    # Process string into integer
    # Example: '12,400,000.0000'  -->  12400000
    data = int(data.replace(',', '').split('.')[0])
    return data
  




add_item("Apples at Walmart", "test_data1.txt")
print(price_data, "\n")


econ_data["Money supply - M3"] = \
    get_stlouisfed_data("https://fred.stlouisfed.org/series/MABMM301USM189S")
econ_data["Monetary base - Currency in Circulation"] = \
    get_stlouisfed_data("https://fred.stlouisfed.org/series/MBCURRCIR")
econ_data["Consumer price index"] = \
    get_stlouisfed_data("https://fred.stlouisfed.org/series/CPIAUCSL")

print(econ_data)




