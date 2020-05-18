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
from tkinter.ttk import *
from tkinter import BOTTOM, Button, Checkbutton, Entry, Frame, IntVar, Label, \
                    LEFT, RIGHT, StringVar, Tk


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
        
    
def to_boolean(var):
    """ Convert strings ('y', 'n') and integers (1, 0) 
        to boolean values (True, False) """
    if type(var) is type("a"):
        var = var.lower().strip()
        if var == "y":
            return True
        else:
            return False
    elif type(var) is type(1):
        if var == 1:
            return True
        else:
            return False
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



# =============================================================================
# GUI Interface
# =============================================================================

def apply_new_item(*args):
    """ Create a new item using the info entered in the new item frame and
        add it to the item list.
    """
    # Get values from the entry boxes
    item_type = item_type_var.get()
    item_description = item_desc_var.get()
    item_unit_quantity = item_unit_var.get()
    is_store_brand = to_boolean(item_sb_var.get())
    store_name = store_var.get()
    store_location = location_var.get()
    
    # Create new item and add it to the item list
    new_item = Item(item_type, item_description, item_unit_quantity,
                    store_name, store_location, is_store_brand)
    item_list[item_description] = new_item
    
    store_matched_items.append(new_item)
    item_entries.append(Item_entry(new_item))
        
    # Refresh the item entry frame
    apply_store_selection()
    

def apply_new_price(*args):
    """ Add a new price entry to the item after entering a price in the
        entry field for that item.
    """
    #new_price = 
    
    
def apply_store_selection(*args):
    """ Search the item list for all items that match the store name
        and location and generate existing item frames for each.
    """
    
    # Destroy any existing item frames
    #for e in item_entries:
    #    e.destroy()
    del item_entries[:]
    clear_exis_item_frame()
    
    # Add message    
    existing_items_label = Label(exis_item_frame, text="Items you've tracked "
                                 "before from this store:", font=("Arial", 16))
    existing_items_label.pack()
    
    # Get list of items from the store provided in the entry boxes
    store = store_var.get()
    location = location_var.get()
    
    
    for i in item_list.values():
        store_match = i.store_name.lower() == store.lower()
        location_match = i.store_location.lower() == location.lower()
        if store_match & location_match:
            # Add item to local items list
            store_matched_items.append(i)
            # Create Item entry object for each item and add to item entries list
            item_entries.append(Item_entry(i))
            
    # Create an existing item frame for each item from matching store
    #for i in items:
    #    create_existing_item_frame(i)
    
    # Add the new item frame to the bottom
    #new_item_frame()


def clear_exis_item_frame():
    """ Destroy any existing item frames """
    existing = exis_item_frame.winfo_children()
    for frame in existing:
        frame.destroy()
    
    
#def create_existing_item_frame(item):
#    """ Pack a frame into the data entry frame representing an item
#        previously added to the item list. This frame contains a description
#        of the item and an entry field for entering a new price to be added
#        to the item's price data.
#    """
#    item_frame = Frame(exis_item_frame)
#    item_frame.pack()
#    
#    label_text = item.item_description.capitalize() + " --- " + \
#                 item.item_unit_quantity + ": $"
#    description_label = Label(item_frame, text=label_text)
#    description_label.grid(row=0, column=0)
#    
#    #price_entry_label = Label(item_frame, text="Enter Price:")
#    #price_entry_label.grid(row=0, column=1)
#    price_entry_box = Entry(item_frame, width=5)
#    price_entry_box.grid(row=0, column=1)
    

def new_item_frame():
    """ Pack a frame into the data entry frame that lets you enter a new
        item you want to track. Contains entry fields for the item's
        type, description, and unit size, and a checkbutton for whether
        the item is a store brand.
    """



class Item_entry:
    
    def __init__(self, item):
        self.item = item
        self.create_existing_item_frame(item)

    def create_existing_item_frame(self, item):
        """ Pack a frame into the data entry frame representing an item
            previously added to the item list. This frame contains a description
            of the item and an entry field for entering a new price to be added
            to the item's price data.
            """
        self.item_frame = Frame(exis_item_frame)
        self.item_frame.pack()
        #item_entry_listbox.insert(self.item_frame)
            
        self.label_text = item.item_description.capitalize() + " --- " + \
                          item.item_unit_quantity + ": $"
        self.description_label = Label(self.item_frame, text=self.label_text)
        self.description_label.grid(row=0, column=0)
        
        if not item.price_entered_already_today():
            # Create a price entry field
            self.price_var = StringVar()
            self.price_entry_box = Entry(self.item_frame, 
                                         textvariable=self.price_var, 
                                         width=5)
            self.price_entry_box.grid(row=0, column=1)
            self.price_entry_box.bind("<Return>", self.apply_price_entry)
        else:
            # Display the price entered already today as text
            self.price_label = Label(self.item_frame, 
                                     text=str(item.price_data[-1][1]))
            self.price_label.grid(row=0, column=1)
            
    def apply_price_entry(self, *args):
        # Get price from entry box
        new_price = float(self.price_var.get())
        
        # Get date from date entry box---convert from string to date first
        d = date.fromisoformat(date_var.get())
        
        # Append date and price to item's price entry list
        self.item.add_price_entry(d, new_price)
        
        # Move text entry focus to the next item for fast data entry
        n = self.price_entry_box.tk_focusNext()
        n.focus_set()
        
        self.price_entry_box.destroy()
        self.price_label = Label(self.item_frame, text=str(new_price))
        self.price_label.grid(row=0, column=1)
        
        
    def destroy(self):
        self.item_frame.destroy()





# =============================================================================
# Run main program
# =============================================================================

    
load()
print("\n Item list: \n", item_list, "\n")
for item in item_list.values():
    item.print_info()
    print("\n")

root = Tk()
root.title("Inflation Predictor")

item_type_var = StringVar()
item_desc_var = StringVar()
item_unit_var = StringVar()
item_sb_var = IntVar()
date_var = StringVar()
store_var = StringVar()
location_var = StringVar()




# Main frame for entering new product and price info
entry_frame = Frame(root)
entry_frame.pack()
entry_frame_title = Label(entry_frame, text="Enter data from your shopping trip:")
entry_frame_title.grid(row=0, columnspan=2)




# Sub-frame of entry frame for entering date and store info
store_frame = Frame(entry_frame, borderwidth=4, relief="ridge")
store_frame.grid(row=1, column=0, pady=30)

date_label = Label(store_frame, text="Date:")
date_label.grid(row=0, column=0, sticky="W", padx=10, pady=10)
date_entry_box = Entry(store_frame, textvariable=date_var)
date_entry_box.insert(1, str(date.today()))
date_entry_box.grid(row=0, column=1)

store_label = Label(store_frame, text="Store name:")
store_label.grid(row=1, column=0, sticky="W")
store_entry_box = Entry(store_frame, textvariable=store_var)
store_entry_box.grid(row=1, column=1)

store_location_label = Label(store_frame, text="Location:")
store_location_label.grid(row=2, column=0, sticky="W")
store_location_entry_box = Entry(store_frame, width=40, 
                                 textvariable=location_var)
store_location_entry_box.grid(row=3, columnspan=2, padx=10, pady=10)
store_location_entry_box.bind("<Return>", apply_store_selection)

store_enter_button = Button(store_frame, 
                            text="Enter", 
                            command=apply_store_selection)
store_enter_button.grid(row=4, column=0, sticky="W")
store_enter_button.bind("<Return>", apply_store_selection)




# Sub-frame of entry frame for entering new product info
""" Pack a frame into the data entry frame that lets you enter a new
    item you want to track. Contains entry fields for the item's
    type, description, and unit size, and a checkbutton for whether
    the item is a store brand.
"""

new_frame = Frame(entry_frame, borderwidth=4, relief="ridge")
new_frame.grid(row=2, column=0, padx=10, pady=10)
    
new_item_label = Label(new_frame, text="Have a new item to track at this "
                          "store? Enter the info below:" )
new_item_label.grid(row=0, column=0, columnspan=2, pady=20)

item_type_label = Label(new_frame, text="The type of product\ne.g.: "
                        "(apple, peanut butter, band-aids, etc.)")
item_type_label.grid(row=1, column=0, sticky="W")
item_type_entry = Entry(new_frame, textvariable=item_type_var)
item_type_entry.grid(row=1, column=1)

item_desc_label = Label(new_frame, text="A more detailed description of "
                        "the item\ne.g.: brand name red delicious apples")
item_desc_label.grid(row=2, column=0, sticky="W")  
item_desc_entry = Entry(new_frame, textvariable=item_desc_var)
item_desc_entry.grid(row=2, column=1)

item_unit_label = Label(new_frame, text="The net weight or number of cont"
                        "ents per item\ne.g.: (12-pack, 30oz)")
item_unit_label.grid(row=3, column=0, sticky="W")
item_unit_entry = Entry(new_frame, textvariable=item_unit_var)
item_unit_entry.grid(row=3, column=1)
    
item_sb_label = Label(new_frame, text="Is the item a store brand?:")
item_sb_label.grid(row=4, column=0, sticky="W")
item_sb_checkbox = Checkbutton(new_frame, variable=item_sb_var)
item_sb_checkbox.var = item_sb_var
item_sb_checkbox.grid(row=4, column=1, sticky="W")

item_enter_button = Button(new_frame, text="Enter", command=apply_new_item)                  
item_enter_button.grid(row=5)
item_enter_button.bind("<Return>", apply_new_item)





# Sub-frame of entry frame for entering existing item price info
exis_item_frame = Frame(entry_frame, borderwidth=4, relief="ridge")
exis_item_frame.grid(row=1, rowspan=2, column=1, padx=5, pady=5)
existing_items_label = Label(exis_item_frame, text="Items you've tracked "
                                 "before from this store:", font=("Arial", 16))
existing_items_label.pack()

exis_item_frame.bind("<Tab>", )





#items_scrollbar = Scrollbar(exis_item_frame)
#items_scrollbar.pack(fill=Y)
#
#item_entry_listbox = Listbox(exis_item_frame,
#                             yscrollcommand=items_scrollbar.set)
#
#items_scrollbar.config(command=item_entry_listbox.yview)

# List of Item objects from given store
store_matched_items = []

# List of Item_entry objects
item_entries = []


#save()

root.mainloop()

