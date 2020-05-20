#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:55:14 2020

@author: JamesButcher
"""
from datetime import date
from collections import namedtuple

class Item:
    """ class Item: a certain product at a store
    
        - item_type:            the type of product, e.g.: (apple, peanut 
                                butter, band-aids, etc.)
        - item_description:     a more detailed description of the item, e.g.:
                                (store brand red delicious apples)
        - item_unit_quantity:   the net weight or number of contents of the
                                product, e.g.: (12-pack, 30oz)
        - store_name:           the name of the store, e.g.: (Walmart, 
                                Target, etc.)
        - store_location:       the location of the store, e.g.: (Wake forest 
                                off of Main street.)
        - is_store_brand:       boolean for whether the product is store brand
        
        - price_data:           a list containing tuple pairs of (date, price)
                                for the price of the item at that date
    """
    
    def __init__(self,
                 item_type,
                 item_description,
                 item_unit_quantity,
                 store_name,
                 store_location,
                 is_store_brand=False):
        self.item_type = item_type
        self.item_description = item_description
        self.item_unit_quantity = item_unit_quantity
        self.store_name = store_name
        self.store_location = store_location
        self.is_store_brand = is_store_brand
        self.price_data = []
        
    def add_price_entry(self, date, price):
        """ Add a named tuple of (date, price) to the list of price data """
        tuple_name = "Price_entry_for_" + \
                     self.item_description.replace(" ", "_")
        price_entry = namedtuple(tuple_name, ["date", "price"])
        self.price_data.append(price_entry(date, price))
        return self.price_data[-1]
    
    def print_info(self):
        print("Item description: \t", self.item_description,
              "\nType: \t\t\t", self.item_type,
              "\nUnit quantity: \t\t", self.item_unit_quantity,
              "\nStore: \t\t\t", self.store_name, self.store_location)
        print("\n Date: \t\t Price:")
        for entry in self.price_data:
            print(entry[0].__str__(), "\t$", entry[1])
    
    def get_price_entry(self, date):
        """ Search the price data for the given date, 
            and return the (date, price) entry if exists """
        for entry in self.price_data:
            year_match = date.year == entry[0].year
            month_match = date.month == entry[0].month
            day_match = date.day == entry[0].day
            
            if year_match & month_match & day_match:
                return entry
        print("No price entry found on that date")
        return None
    
    def price_entered_already_today(self):
        """ returns True if a price entry was added today """
        if len(self.price_data) == 0:
            return False
        todays_date = date.today()
        latest_entry_date = max([entry[0] for entry in self.price_data])
        if todays_date == latest_entry_date:
            return True
        else:
            return False
        
    def print_price_data(self):
        print("   Date: \t   Price:")
        for entry in self.price_data:
            print(" {}  --  ${: 8.2f}".format(entry[0], entry[1]))
            
    def remove_todays_price_entry(self):
        del self.price_data[-1]
            
    def to_string(self):
        """ Convert item's data attributes into formatted string for saving """
        attributes = [self.item_type, self.item_description,
                      self.item_unit_quantity, self.store_name,
                      self.store_location, self.is_store_brand]

        string = "" 
        for att in attributes:
            string = string + str(att) + "\n"
            
        for entry in self.price_data:
            string = string + entry[0].__str__() + ", " + str(entry[1]) + "\n"
            
        return string
        
        
        
    