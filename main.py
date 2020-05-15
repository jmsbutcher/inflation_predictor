#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:22:44 2020

@author: JamesButcher
"""


#import numpy as np
#import pandas as pd
#import requests
#from bs4 import BeautifulSoup
from datetime import date
#from matplotlib import pyplot
from pathlib import Path
from tkinter import *
from tkinter import Entry, Frame, Label

from item import Item

item_list = {}


"""
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
    # Process string into integer
    # Example: '12,400,000.0000'  -->  12400000
    data = int(data.replace(',', '').split('.')[0])
    return data

econ_data["Money supply - M3"] = \
    get_stlouisfed_data("https://fred.stlouisfed.org/series/MABMM301USM189S")
econ_data["Monetary base - Currency in Circulation"] = \
    get_stlouisfed_data("https://fred.stlouisfed.org/series/MBCURRCIR")
econ_data["Consumer price index"] = \
    get_stlouisfed_data("https://fred.stlouisfed.org/series/CPIAUCSL")

print(econ_data)
"""

def add_price_entry(item_description, date, price):
    if item_description in item_list:
        item_list[item_description].add_price_entry(date, price)
    else:
        print("ERROR : Item does not exist.  >", item_description)


def enter_shopping_trip_data_manually():
    """ Use the keyboard to enter data manually.
          Step 1: Get store information and date from keyboard input.
          Step 2: (Loop) Get item information and price from keyboard input,
                  create new item object, add it to the item list, and add
                  a price entry to it.
          Step 3: Print the store and item info to standard output
    """
    # Get the store information
    store_name = input("Enter the name of the store: ").lower()
    store_location = input("Enter the store location: ").lower()
    trip_was_today = input("Was the shopping trip today? [y/n] ").lower()
    if trip_was_today:
        shopping_date = date.today()
    else:
        shopping_date = date.fromisoformat(input("Enter the date of the "
            "shopping trip: yyyy-mm-dd\n"))
        
    # Start loop for creating items 
    while True:
        # Enter item information
        item_type = input(
            "Enter the type of product,"
            "e.g.: (apple, peanut butter, band-aids, etc.)\n").lower()
        item_description = input(
            "Enter a more detailed description of the item,"
            "e.g.: (store brand red delicious apples)\n").lower()
        item_unit_quantity = input(
            "Enter the net weight or number of contents of the product,"
            "e.g.: (12-pack, 30oz, etc.)\n").lower()
        is_store_brand = input(
            "Is the item a store brand? [y/n] ").lower()
        if is_store_brand == "y":
            is_store_brand = True
        else:
            is_store_brand = False
        item_price = input("Enter the price of the product: $")
        
        # Create new Item object using the info just entered plus
        #   the store info entered earlier
        new_item = Item(item_type, item_description, item_unit_quantity,
                        store_name, store_location, is_store_brand)
        # Add new item to the item list dictionary using the item
        #   description as the key and the item object as the value
        item_list[item_description] = new_item
        
        # Add date and price to the item's list of price entries
        new_item.add_price_entry(shopping_date, item_price)
        
        more_items_to_add = to_boolean(input("Enter another item? [y/n]: "))
        if not more_items_to_add:
            break
        
def load():
    """ Load saved item data into item_list """
    folder = Path.cwd() / "items"
    filenames = folder.glob("*.txt")
    for file in filenames:
        with open(file, "r") as f:
            # Read item attribute data (description, store, unit quantity, etc)
            item_type = f.readline().strip("\n")
            item_description = f.readline().strip("\n")
            item_unit_quantity = f.readline().strip("\n")
            store_name = f.readline().strip("\n")
            store_location = f.readline().strip("\n")
            is_store_brand = bool(f.readline().strip("\n"))
                
            #Create Item object using loaded attributes
            loaded_item = Item(item_type, item_description, item_unit_quantity,
                               store_name, store_location, is_store_brand)
            
            # Add loaded item to item_list
            item_list[item_description] = loaded_item
            
            # Read price data from remaining lines
            for line in f:
                entry = line.strip("\n").split(", ")
                shopping_date = date.fromisoformat(entry[0])
                price = float(entry[1])
                loaded_item.add_price_entry(shopping_date, price)
                
        
        
def save():
    """ Save item data to item folder """
    folder = Path.cwd() / "items"
    
    # Create a file for each item, titled "[description].txt"
    for description, item in item_list.items():
        filename = folder / (description.lower().replace(" ", "_") + ".txt")
        with open(filename, "w") as f:
            f.write(item.to_string())
        
    
def to_boolean(string):
    """ Convert strings ('y', 'n') to boolean values (True, False) """
    string = string.lower().strip()
    if string == "y":
        return True
    else:
        return False
    


"""
a = Item("apples", "Rosy Farms red delicious apples", "12-pack", "Walmart",
         "Wake forest off Main Street")
a.add_price_entry(date.today(), 3.49)
a.add_price_entry(date(2020, 4, 25), 3.29)
a.add_price_entry(date(2020, 4, 11), 13.19)
a.print_price_data()

b = Item("soymilk", "organic unsweetened soymilk", "1 gallon", "Target",
         "around the block", True)
b.add_price_entry(date.today(), 2.29)
b.add_price_entry(date(2020, 5, 3), 2.29)
b.print_price_data()

item_list[a.item_description] = a
item_list[b.item_description] = b
"""



#save()
load()
add_price_entry("organic unsweetened soymilk", date(2020, 10, 10), 99.99)


print("\n Item list: \n", item_list, "\n")
for item in item_list.values():
    item.print_info()
    print("\n")
    
    
def create_existing_item_frame(item):
    item_frame = Frame(entry_frame)
    item_frame.pack()
    
    label_text = item.item_description.capitalize() + " --- " + \
                 item.item_unit_quantity
    description_label = Label(item_frame, text=label_text)
    description_label.grid(row=0, columnspan=4)
    
#    date_label = Label(item_frame, text="Date:")
#    date_label.grid(row=1, column=0)
#    date_entry_box = Entry(item_frame)
#    date_entry_box.insert(1, str(date.today()))
#    date_entry_box.grid(row=1, column=1)
    
    price_entry_label = Label(item_frame, text="Enter Price:")
    price_entry_label.grid(row=1, column=2)
    price_entry_box = Entry(item_frame)
    price_entry_box.grid(row=1, column=3)
    
def new_item_frame():
    new_frame = Frame(entry_frame)
    new_frame.pack()
    
    new_item_label = Label(new_frame, text="Have a new item to track at this "
                           "store? Enter the info below:" )
    new_item_label.grid(row=0, column=0, columnspan=2, pady=20)

    item_type_label = Label(new_frame, text="The type of product\ne.g.: "
                            "(apple, peanut butter, band-aids, etc.)")
    item_type_label.grid(row=1, column=0, sticky="W")
    item_type_entry = Entry(new_frame)
    item_type_entry.grid(row=1, column=1)

    item_desc_label = Label(new_frame, text="A more detailed description of "
                            "the item\ne.g.: brand name red delicious apples")
    item_desc_label.grid(row=2, column=0, sticky="W")  
    item_desc_entry = Entry(new_frame)
    item_desc_entry.grid(row=2, column=1)

    item_unit_label = Label(new_frame, text="The net weight or number of cont"
                            "ents per item\ne.g.: (12-pack, 30oz)")
    item_unit_label.grid(row=3, column=0, sticky="W")
    item_unit_entry = Entry(new_frame)
    item_unit_entry.grid(row=3, column=1)

    item_sb_label = Label(new_frame, text="Is the item a store brand?:")
    item_sb_label.grid(row=4, column=0, sticky="W")
    item_sb_checkbox = Checkbutton(new_frame)
    item_sb_checkbox.grid(row=4, column=1, sticky="W")                    




root = Tk()
root.title("Inflation Predictor")

# Frame for entering new product and price info
entry_frame = Frame(root)
entry_frame.pack()
entry_frame_title = Label(entry_frame, text="Enter data from your shopping trip:")
entry_frame_title.pack()

store_frame = Frame(entry_frame, borderwidth=4, relief="ridge")
store_frame.pack(pady=30)

date_label = Label(store_frame, text="Date:")
date_label.grid(row=0, column=0, sticky="W", padx=10, pady=10)
date_entry_box = Entry(store_frame)
date_entry_box.insert(1, str(date.today()))
date_entry_box.grid(row=0, column=1)
store_label = Label(store_frame, text="Store name:")
store_label.grid(row=1, column=0, sticky="W")
store_entry_box = Entry(store_frame)
store_entry_box.grid(row=1, column=1)
store_location_label = Label(store_frame, text="Location:")
store_location_label.grid(row=2, column=0, sticky="W")
store_location_entry_box = Entry(store_frame, width=40)
store_location_entry_box.grid(row=3, columnspan=2, padx=10, pady=10)

# Create an existing item frame for each item already saved
existing_items_label = Label(entry_frame, text="Items you've tracked before "
                             "from this store:", font=("Arial", 16))
existing_items_label.pack()
for item in item_list.values():
    create_existing_item_frame(item)

new_item_frame()


root.mainloop()

