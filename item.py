#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:55:14 2020

@author: JamesButcher
"""

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
        
        - price_data:           a dictionary containing pairs of date : price
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
        self.price_data = {}
        
    def __repr__(self):
        """ Convert item's data into formatted string for saving """
        attributes = [self.item_type, self.item_description,
                      self.item_unit_quantity, self.store_name,
                      self.store_location, self.is_store_brand]
        string = "" 
        for att in attributes:
            string = string + str(att) + "\n"
            
        sorted_dates = sorted(self.price_data)
        for date_entry in sorted_dates:
            price = "{:>5.2f}".format(self.price_data[date_entry])
            string = string + date_entry.__str__() + ", " + price + "\n"
            
        return string      
    
    def __str__(self):
        """ Print all item attributes and price data in a readable way"""
        string = "Item description: \t" + self.item_description + \
                 "\nType: \t\t\t" + self.item_type + \
                 "\nUnit quantity: \t\t" + self.item_unit_quantity + \
                 "\nStore: \t\t\t" + self.store_name + " " + self.store_location + \
                 "\n Date: \t\t Price:\n"
        sorted_dates = sorted(self.price_data)
        for date_entry in sorted_dates:
            price = "{:>5.2f}".format(self.price_data[date_entry])
            string += str(date_entry) + "\t$" + price + "\n"
            
        return string    
    
    def add_price_entry(self, date_entry, price):
        """ Add a price entry to the price_data dict 
        
            { date_entry[type=date] : price[type=float] }
        """
        self.price_data[date_entry] = price
 
    def remove_price_entry(self, removal_date):
        """ Remove price entry at removal_date """
        del self.price_data[removal_date]
    