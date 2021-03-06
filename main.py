#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:22:44 2020

@author: JamesButcher

A Python app that tracks, analyzes, and predicts future price trends of 
ordinary consumer products using machine learning.

- The user enters the prices of his or her favorite items at the store after 
    every shopping trip into a user-friendly GUI.
- The program keeps track of the item, the store, the date, and the price.
- On command, the program scrapes a set of economic data points from the web 
    and bundles it all into a machine learning training set.
- The program performs a linear regression algorithm and displays a future 
    price trend on an individual item basis. Key timeframes are highlighted, 
    e.g. "The 5lb bag of Red delicious apples from the Wake forest Walmart is 
    predicted to cost $6.44 a month from now."

"""

import matplotlib
import matplotlib.dates as mdates
import numpy as np
#import pandas as pd
from datetime import date, timedelta
from pathlib import Path
from tkinter import BOTH, Button, Checkbutton, DISABLED, DoubleVar, END, \
                    Entry, Frame, IntVar, Label, LEFT, NORMAL, RIGHT, \
                    Spinbox, StringVar, Tk, TOP, N, S, E, W, X, Y
from tkinter.ttk import Combobox

#import data_analysis
from data_analysis import predict_single_item
from item import Item

# Dictionary of Item objects --- { [Item.item_description1] : [Item1], ...  }
item_list = {}


# =============================================================================
# General functions
# =============================================================================
def apply_new_item(*events):
    """ Create a new item using the info entered in the new item frame and
        add it to the item list.
    """
    # Get values from entry boxes
    item_type = item_type_entry.get_text()
    item_description = item_desc_entry.get_text()
    item_unit_quantity = item_unit_entry.get_text()
    
    is_store_brand = to_boolean(item_storebrand_var.get())
    store_name = store_var.get()
    store_location = location_var.get()
    
    # Create new item and add it to the item list
    new_item = Item(item_type, item_description, item_unit_quantity,
                    store_name, store_location, is_store_brand)
    item_list[item_description] = new_item
    
    store_matched_items.append(new_item)
    item_entries.append(Item_entry(new_item))

    # Clear text from data entry fields
    item_type_entry.reset()
    item_desc_entry.reset()
    item_unit_entry.reset()
    
    # Move text entry focus back to top for fast data entry
    item_type_entry.set_focus()
    
def apply_store_selection(*events):
    """ Search the item list for all items that match the store name
        and location selected and generate Item_entrys for each.
    """
    # Remove blue "Saved" message, indicating a new saveable change
    saved_label.grid_remove()
    # Enable save button and other widgets
    enable(save_button, 
           existing_items_label, 
           *new_frame.winfo_children(), 
           item_select_label, item_select_box,
           timeframe_select_label, timeframe_select_box,
           plot_button)
    item_select_box.configure(foreground="black")
    timeframe_select_box.configure(foreground="black")
           
    # Remove any existing plots from prediction frame
    ax.cla()
    # Clear saved training set
    global old_training_set
    old_training_set = None
    
    # Enable all the entry fields in new item entry frame
#    for item_entry in item_entries:
#        item_entry.enable_widgets()
    
    # Reset the item entry frame    
    del item_entries[:]
        
    for widget in exis_item_frame.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()

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
            
    # Load items from store into the item selection box in predict frame
    load_items()
    
def change_state(*widgets, new_state):
    for widget in widgets:
        if isinstance(widget, list):
            for w in widget:
                w.configure(state=new_state)
        else:
            widget.configure(state=new_state)
            
def disable(*widgets):
    change_state(*widgets, new_state=DISABLED)
    
def enable(*widgets):
    change_state(*widgets, new_state=NORMAL)
    
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

 
def plot_prices():
    """ Plot prices vs. date for selected item """
    # Get item from item list matching item description in selection box
    item = item_list[item_predict_var.get()]
    # Get timeframe in days from timeframe selection box
    timeframe = timeframes[timeframe_var.get()]
    
    # Clear any previous plot
    ax.cla()

    # x = Dates, y = Prices
    x = sorted(item.price_data)
    y = [item.price_data[date_entry] for date_entry in x]
    
    timerange = (max(x) - min(x)).days + timeframe
    
    ax.plot(x, y, 'bo-')
    
    ax.set_title("Price trend for {}".format(item.item_description), fontsize=18)
    ax.set_xlabel("Date", fontsize=16)
    ax.set_ylabel("Price in $", fontsize=16)
    
    x_lower_bound = min(x) - timedelta(days=int(0.05*timerange))
    x_upper_bound = date.today() + timedelta(days=timeframe+int(0.05*timerange))

    ax.set_xlim([x_lower_bound, x_upper_bound])
    
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    
    if timerange > 1000:
        years_format = mdates.DateFormatter("'%y") # E.g.: '20
        months_format = mdates.DateFormatter("")
    elif timerange > 500:
        years_format = mdates.DateFormatter("%Y")  # E.g.: 2020
        months_format = mdates.DateFormatter("")
    else:
        years_format = mdates.DateFormatter("%Y")  # E.g.: Jun 2020
        months_format = mdates.DateFormatter("%b")
    
    # Format axes
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_format)
    ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_minor_formatter(months_format)
    ax.tick_params(which="major", length=16, width=1)
    ax.tick_params(which="minor", length=4, width=2, color="b")
    ax.grid(True)
    
    toolbar.update()
    plot_price_trend()
    enable(plot_controls)
    

def plot_price_trend():
    """ Plot a linear or polynomial regression trendline of price vs. date """
    global trendline
    # Get item from item list matching item description in selection box
    item = item_list[item_predict_var.get()]
    # Get timeframe in days from timeframe selection box
    timeframe = timeframes[timeframe_var.get()]
    # Get polynomial order from spinbox
    polynomial_order = int(polynomial_order_spinbox.get())
    
    # x = Dates, y = Prices
    x = sorted(item.price_data)
    y = [item.price_data[date_entry] for date_entry in x]
    
    earliest_date = min(x)
    latest_date = date.today() + timedelta(days=timeframe)
    
    daterange = latest_date - earliest_date
    dayrange = daterange.days
    num_bins = 50
    if dayrange <= num_bins:
        stride = 1
    else:
        stride = int(dayrange / num_bins)
    
    # Convert list of dates into int list of days since first date
    days_since_earliest = []
    for d in x:
        elapsed = d - x[0]
        days_since_earliest.append(elapsed.days)
    
    # Perform linear regression (or polynomial reg. if polynomial_order > 1)
    regression_model = np.polyfit(days_since_earliest, y, polynomial_order)
    regression_line = np.poly1d(regression_model)
    
    x_line = list(range(0, dayrange, stride))
    
    date_line = []
    for i in range(len(x_line)):
        date_line.append(earliest_date + timedelta(days=i*stride))
    
    # Either plot trendline or remove trendline depending on checkbutton state    
    if len(trendline) > 0:
        line = trendline.pop(0)
        line.remove()
        del line
    if to_boolean(show_trendline_var.get()):
        trendline = ax.plot(date_line, regression_line(x_line), "k--")

    plot_canvas.draw()
    
               
def predict(*events):
    """ Use multivariate linear regression to predict price of item """
    # Get item from item list matching item description in selection box
    item = item_list[item_predict_var.get()]
    # Get timeframe in days from timeframe selection box
    timeframe = timeframes[timeframe_var.get()]
    # Get polynomial order from spinbox
    polynomial_order = int(polynomial_order_spinbox.get())
    # Get regularization coefficient
    regularization_coeff = float(regularization_var.get())
    
    # Saved training set for quick reuse
    global old_training_set
    
    dates, prediction, curve, training_set = predict_single_item(item, 
                                                        timeframe, 
                                                        polynomial_order,
                                                        regularization_coeff,
                                                        old_training_set)
    
#    prediction_text = ("Predicted price:\n${:.2f}".format(float(prediction)))
    prediction_text = ("${:.2f}".format(float(prediction)))

#    item_text = item_predict_var.get
    timeframe_text = timeframe_var.get()
    date_text = str(date.today() + timedelta(days=timeframe))
    
    prediction_result_text = "Predicted price for {}\non {}, {}:\n{}".format( \
                             item, date_text, timeframe_text, prediction_text)
    #result_label.configure(text=prediction_result_text)    
    
    ax.plot(dates, curve, "r--")
    ax.plot(dates[-1], prediction, "k*")
    
    ax.text(date.today() + timedelta(days=timeframe), 
            float(prediction), 
            prediction_text)
    
    plot_canvas.draw()
    
    old_training_set = training_set
                
def save(*events):
    """ Save all item data to item folder """
    print("Saving...")
    folder = Path.cwd() / "items"
    # Create a file for each item, titled "[description].txt"
    for description, item in item_list.items():
        filename = folder / (description.lower().replace(" ", "_") + ".txt")
        with open(filename, "w") as f:
            f.write(repr(item))
    print("Save complete")
    
    # Display blue "Saved" message in bottom right corner of GUI
    saved_label.grid(row=3, column=2)
    disable(save_button)

def to_boolean(var):
    """ Convert strings ('y', 'n') and integers (1, 0) to boolean values """
    if isinstance(var, str):
        var = var.lower().strip()
        if var == "y":
            return True
        elif var == "n":
            return False
        else:
            print("ERROR: String must be either 'y' or 'n'. You entered:", var)
            return False
    elif isinstance(var, int):
        if var == 1:
            return True
        elif var == 0:
            return False
        else:
            print("ERROR: Integer must be either 1 or 0. You entered:", var)
            return False
    else:
        print("ERROR: to_boolean(var) only accepts 'y', 'n', 0, or 1. You "
              "entered a", type(var), "-->", var)
        return False
    

class Item_entry:
    """ A frame for entering or editing the price of an item. """
    
    def __init__(self, item):
        self.item = item
        self.create_existing_item_frame(item)

    def create_existing_item_frame(self, item):
        """ Pack a frame into the data entry frame representing an item
            previously added to the item list. This frame contains a 
            description of the item and an entry field for entering a 
            new price to be added to the item's price data.
        """
        # Remove blue "Saved" message, indicating a new saveable change  
        saved_label.grid_remove()
        # Create and place frame
        self.item_frame = Frame(exis_item_frame)
        self.item_frame.pack()
        # Label example: " Whole wheat wonder bread  -  1 loaf: $ "
        self.label_text = item.item_description.capitalize() + "  -  " + \
                          item.item_unit_quantity + ": $"
        self.description_label = Label(self.item_frame, text=self.label_text,
                                       wraplength=300)
        self.description_label.grid(row=0, column=0)

        d = date.fromisoformat(date_var.get())
        if d in item.price_data:
            self.generate_price_label_box()
        else:
            self.generate_price_entry_box()
            
    def apply_price_entry(self, *events):
        """ Enter the price in the entry box to the item's price list """
        # Remove blue "Saved" message, indicating a new saveable change
        saved_label.grid_remove()
        # Get price from entry box
        new_price = float(self.price_var.get())
        # Get date from date entry box---convert from String to Date first
        d = date.fromisoformat(date_var.get())
        # Append date and price to item's price entry list
        self.item.add_price_entry(d, new_price)
        # Move focus to the next item entry box for fast data entry
        next_widget = self.price_entry_box.tk_focusNext()
        while next_widget["text"] == "Edit":
            next_widget = next_widget.tk_focusNext()
        next_widget.focus_set()
        # Replace price entry box with a text label of the price just entered
        self.price_entry_box.destroy()
        self.generate_price_label_box()   
        self.clear_saved_training_set()
    
    def clear_saved_training_set(self):
        if self.item.item_description == item_predict_var.get():
            global old_training_set
            old_training_set = None
            
    def disable_widgets(self):
        print("ITem entry disabled")
        for widget in self.item_frame.winfo_children():
            widget.configure(state=DISABLED)
    
    def enable_widgets(self):
        print("ItEm entry enAbled")
        for widget in self.item_frame.winfo_children():
            widget.configure(state=NORMAL)
        
    def edit(self, *events):
        """ Remove price entry from item object and update entry widgets """
        self.item.remove_price_entry(date.fromisoformat(date_var.get()))
        self.price_label.destroy()
        self.edit_button.destroy()
        self.generate_price_entry_box()
        self.price_entry_box.focus_set()
        self.clear_saved_training_set()

    def generate_price_entry_box(self):
        """ Create and place a price entry box """
        self.price_var = StringVar()
        self.price_entry_box = Entry(self.item_frame, 
                                     textvariable=self.price_var, 
                                     width=5)
        self.price_entry_box.grid(row=0, column=1)
        self.price_entry_box.bind("<Return>", self.apply_price_entry)
  
    def generate_price_label_box(self):
        """ Create and place a price label box
        
            - Create and place a text label of the price for given date
            - Create and place an Edit button
        """
        entry_date = date.fromisoformat(date_var.get())
        price = self.item.price_data[entry_date]
        price_text = "{:.2f}".format(price)
        self.price_label = Label(self.item_frame, text=price_text)
        self.price_label.grid(row=0, column=1)
        
        self.edit_button = Button(self.item_frame, 
                                  text="Edit", 
                                  command=self.edit)
        self.edit_button.grid(row=0, column=2)
        self.edit_button.bind("<Return>", self.edit)
    
        
        
# =============================================================================
# Run main program
# =============================================================================

load()

# Print all existing item info 
print()
for item in item_list.values():
    print(str(item), "\n")
    

# =============================================================================
# Set up GUI
# =============================================================================
root = Tk()
root.title("Inflation Predictor")

# List of Item objects that match selected store
store_matched_items = []

# List of Item_entry objects currently in the price entry frame
item_entries = []

# Saved training set for quick reuse
old_training_set = None

# Entry field variables
date_var = StringVar()
store_var = StringVar()
location_var = StringVar()
item_type_var = StringVar()
item_desc_var = StringVar()
item_predict_var = StringVar()
item_unit_var = StringVar()
item_storebrand_var = IntVar()
regularization_var = DoubleVar()
show_trendline_var = IntVar()
timeframe_var = StringVar()




# =============================================================================
# Entry frame: Main frame for entering new product and price info
# =============================================================================
entry_frame = Frame(root, bg="#999999", borderwidth=4, relief="sunken")
entry_frame.pack(side=LEFT, anchor=W, expand=1, fill=Y)
entry_frame_title = Label(entry_frame, font=("Arial", 20, "bold"),
                          fg="white", bg="#999999",
                          text="Enter data from shopping trip:")
entry_frame_title.grid(row=0, columnspan=2)


# =============================================================================
# Sub-frame of entry frame:
#   Date and store selector
# =============================================================================
store_frame = Frame(entry_frame, borderwidth=4, relief="ridge")
store_frame.grid(row=1, column=0, ipady=5, ipadx=5)

date_label = Label(store_frame, text="Date:")
date_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
date_entry_box = Entry(store_frame, textvariable=date_var)
date_entry_box.insert(1, str(date.today()))
date_entry_box.grid(row=0, column=1, sticky=W)

store_label = Label(store_frame, text="Store name:")
store_label.grid(row=1, column=0, sticky=W)

# Select from a list of all the different stores found in the item list
store_entry_box = Combobox(store_frame, textvariable=store_var)
store_entry_box.grid(row=1, column=1, sticky=W)
stores = {s.store_name for s in item_list.values()}
store_entry_box["values"] = tuple(stores)
store_entry_box.current(0)
#store_entry_box.bind("<<ComboboxSelected>>", load_store_locations)

store_location_label = Label(store_frame, text="Location:")
store_location_label.grid(row=2, column=0, sticky=W)
store_location_entry_box = Combobox(store_frame, width=27, 
                                 textvariable=location_var)
store_location_entry_box.grid(row=2, column=1, pady=5, sticky=W)
#load_store_locations()

store_enter_button = Button(store_frame, text="Enter", 
                            command=apply_store_selection)
store_enter_button.grid(row=4, columnspan=2)
store_enter_button.bind("<Return>", apply_store_selection)


# ============================================================================= 
# Sub-frame of entry frame:
#   New product adder
# =============================================================================
new_frame = Frame(entry_frame, borderwidth=4, relief="ridge")
new_frame.grid(row=2, column=0, padx=10, pady=10)

new_item_label = Label(new_frame, text="Have a new item to track at this "
                                       "store?\nEnter the info below:")
new_item_label.grid(row=0, column=0, columnspan=2, pady=20) 



class New_item_entry:
    example_text_color = "#CCCCCC"
    
    def __init__(self, row, label_text, example_text, width=40):
        self.row = row
        self.label_text = label_text
        self.example_text = example_text
        self.width = width
        self.var = StringVar()
        self.create_label()
        self.create_entry()
        
    def create_label(self):
        self.label = Label(new_frame, text=self.label_text)
        self.label.grid(row=self.row, columnspan=2, pady=3, padx=10, sticky=W)
        
    def create_entry(self):
        self.entry = Entry(new_frame, textvariable=self.var, width=self.width,
                           foreground=self.example_text_color)
        self.entry.grid(row=self.row + 1, columnspan=2, padx=5, sticky=W)
        self.entry.insert(0, self.example_text)
        self.entry.bind("<FocusIn>", self.focus_in)
        self.entry.bind("<FocusOut>", self.focus_out)
        self.entry.bind("<Return>", self.move_to_next)
      
    def focus_in(self, *events):
        if self.var.get() == self.example_text:
            self.entry.delete(0, END)
            self.entry.configure(foreground="black")
        
    def focus_out(self, *events):
        if len(self.var.get()) == 0:
            self.reset()
            
    def get_text(self):
        # Return contents of the entry field if default text has been changed.
        if self.var.get() == self.example_text:
            return("")
        else:
            return self.var.get()    
    
    def reset(self):
        self.entry.delete(0, END)
        self.entry.insert(0, self.example_text)
        self.entry.configure(foreground=self.example_text_color)
        
    def set_focus(self):
        self.entry.focus_set()
        
    def move_to_next(self, *events):
        next_widget = self.entry.tk_focusNext()
        next_widget.focus_set()

item_type_entry = New_item_entry(1, "The type of product:",
                            "e.g.: (apple, peanut butter, band-aids, etc.)")
item_desc_entry = New_item_entry(3, "A more detailed description:",
                            "e.g.: (brand name red delicious apples)")
item_unit_entry = New_item_entry(5, "Net weight or number of contents "
                            "per item:", "e.g.: (12-pack, 30oz)", width=30)

    
def toggle_storebrand_checkbox(*events):
    item_sb_checkbox.toggle()

item_sb_label = Label(new_frame, text="Is the item a store brand?:")
item_sb_label.grid(row=7, column=0, padx=10, sticky=W)
item_sb_checkbox = Checkbutton(new_frame, variable=item_storebrand_var)
item_sb_checkbox.var = item_storebrand_var
item_sb_checkbox.grid(row=7, column=1, sticky="W")
item_sb_checkbox.bind("<Return>", toggle_storebrand_checkbox)

item_enter_button = Button(new_frame, text="Enter", command=apply_new_item)                  
item_enter_button.grid(row=8, pady=5)
item_enter_button.bind("<Return>", apply_new_item)

disable(*new_frame.winfo_children())


# =============================================================================
# Sub-frame of entry frame:
#   List of existing items tracked at selected store
#   Used for price entry
# =============================================================================
exis_item_frame = Frame(entry_frame, borderwidth=4, relief="ridge")
exis_item_frame.grid(row=1, rowspan=2, column=1, padx=5, sticky=N)

# Add title message    
existing_items_label = Label(exis_item_frame, font=("Arial", 16),
                             text="Items previously tracked from this store:",
                             state=DISABLED)
existing_items_label.pack()

# Save button that writes all item and their corresponding price data 
#   to files in the items folder
save_button = Button(entry_frame, text="Save", command=save)
save_button.grid(row=3, column=1, sticky="SE", padx=5, pady=5)
save_button.bind("<Return>", save)

# A blue "Saved" message that appears only after pressing the save button
saved_label = Label(entry_frame, text="Saved", foreground="blue")


def load_store_locations(*events):
    """ Load all the locations previously saved for the selected store
        
        Create a set of store locations that contains all the store locations
        saved in the item list for the store name currently selected in the 
        store selection combobox, and list those store locations in the 
        store location combobox.
    """

    store_locations = {i.store_location for i in item_list.values() if \
                       i.store_name == store_var.get()}
    store_location_entry_box["values"] = tuple(store_locations)
    store_location_entry_box.current(0)
    
    disable(*new_frame.winfo_children())
    disable(existing_items_label)
    for item_entry in item_entries:
        item_entry.disable_widgets()
        
store_entry_box.bind("<<ComboboxSelected>>", load_store_locations)

load_store_locations()


# =============================================================================
# Prediction frame: Main frame for making predictions about item prices
# =============================================================================
predict_frame = Frame(root, bg="#999999", borderwidth=4, relief="sunken")
predict_frame.pack(side=LEFT, fill=BOTH, expand=1)

predict_frame_title = Label(predict_frame, font=("Arial", 20, "bold"),
                            fg="white", bg="#999999",
                            text="Make Price Predictions:")
predict_frame_title.grid(row=0, column=0)



# =============================================================================
# Sub-frame of predict_frame:
#   Control frame for selecting item and prediction parameters
# =============================================================================
predict_control_frame = Frame(predict_frame, borderwidth=4, relief="ridge")
predict_control_frame.grid(row=1, column=0, padx=5, pady=10)

def load_items(*events):
    items = {i.item_description for i in item_list.values() if \
             i.store_name == store_var.get() and \
             i.store_location == location_var.get()}
    item_select_box["values"] = tuple(items)
    item_select_box.current(0)
    
def reset_saved_training_set(*events):
    global old_training_set
    old_training_set = None
    print("RESET TRAINING SET")
    disable(plot_controls)
    
def disable_plot_controls(*events):
    disable(plot_controls)

item_select_label = Label(predict_control_frame, text="Select item:")
item_select_label.grid(row=0, column=0, sticky=W)
item_select_box = Combobox(predict_control_frame, width=30,
                           textvariable=item_predict_var,
                           foreground="gray")
item_select_box.grid(row=0, column=1, columnspan=3, sticky=W)
item_select_box.bind("<<ComboboxSelected>>", reset_saved_training_set)
load_items()

timeframe_select_label = Label(predict_control_frame, text="Select timeframe:")
timeframe_select_label.grid(row=1, column=0, sticky=W)
timeframe_select_box = Combobox(predict_control_frame, 
                                textvariable=timeframe_var,
                                foreground="gray")
timeframe_select_box.grid(row=1, column=1, columnspan=3, sticky=W)
timeframes = {"Today":                0,
              "1 month from today":   30,
              "3 months from today":  91,
              "1 year from today":    365,
              "3 years from today":   1096,
              "10 years from today":  3652}
timeframe_select_box["values"] = tuple(timeframes.keys())
timeframe_select_box.current(0)
timeframe_select_box.bind("<<ComboboxSelected>>", disable_plot_controls)

plot_button = Button(predict_control_frame, text="Plot", command=plot_prices)
plot_button.grid(row=2, column=1, columnspan=1, pady=5)

def toggle_show_trendline_checkbox(*events):
    show_trendline_checkbox.toggle()

show_trendline_label = Label(predict_control_frame, text="Show price trendline:")
show_trendline_label.grid(row=2, column=2, sticky=E)
show_trendline_checkbox = Checkbutton(predict_control_frame,
                                      variable=show_trendline_var,
                                      state=DISABLED,
                                      command=plot_price_trend,
                                      activeforeground="orange",
                                      activebackground="red", 
                                      disabledforeground="green",
                                      foreground="purple",
                                      highlightbackground="yellow")
show_trendline_checkbox.var = show_trendline_var
show_trendline_checkbox.grid(row=2, column=3, sticky=W)
show_trendline_checkbox.bind("<Return>", toggle_show_trendline_checkbox)

polynomial_order_label = Label(predict_control_frame, text="Polynomial order:")
polynomial_order_label.grid(row=3, column=1, columnspan=2, sticky=W)
polynomial_order_spinbox = Spinbox(predict_control_frame, 
                                   from_=1, to=5, width=2,
                                   command=plot_price_trend)
polynomial_order_spinbox.grid(row=3, column=3, sticky=W)

regularization_label = Label(predict_control_frame, text="Regularization "
                                                         "coefficient:")
regularization_label.grid(row=4, column=1, columnspan=2, sticky=W)
regularization_entry = Entry(predict_control_frame, 
                             textvariable=regularization_var,
                             width=5)
regularization_entry.grid(row=4, column=3, columnspan=1, sticky=W)

predict_button = Button(predict_control_frame, text="Predict", command=predict)
predict_button.grid(row=5, column=1, columnspan=1, padx=5, pady=5)

disable(*predict_control_frame.winfo_children())

plot_controls = [#timeframe_select_label, timeframe_select_box,
                 polynomial_order_label, polynomial_order_spinbox,
                 show_trendline_label, show_trendline_checkbox,
                 regularization_label, regularization_entry,
                 predict_button]


# =============================================================================
# Sub-frame of predict_frame:
#   Results and message frame
# =============================================================================


#results_frame = Frame(predict_frame, borderwidth=4, relief="ridge")
#results_frame.grid(row=1, column=1)
#
#result_label = Label(results_frame)
#result_label.pack()


# =============================================================================
# Sub-frame of predict frame:
#   Plot
# =============================================================================

plot_frame = Frame(predict_frame, borderwidth=4, relief="raised")
plot_frame.grid(row=2, columnspan=2, padx=10, pady=10)

# For embedding Matplotlib Figure into Tkinter Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

plot_figure = Figure(figsize=(8, 6), dpi=80)

plot_canvas = FigureCanvasTkAgg(plot_figure, master=plot_frame)

plot_canvas.get_tk_widget().pack(fill=BOTH, expand=1)

toolbar = NavigationToolbar2Tk(plot_canvas, plot_frame)
toolbar.update()
plot_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


def on_key_press(event):
    key_press_handler(event, plot_canvas, toolbar)


plot_canvas.mpl_connect("key_press_event", on_key_press)

ax = plot_figure.add_subplot()
trendline = ax.plot()





# =============================================================================
#   Test command box




#print(data_analysis.convert_price_data_to_training_set(list(item_list.values())[1]))

#data_analysis.convert_price_data_to_training_set(list(item_list.values())[2])

#for item in item_list.values():
#    generate_training_set(item, 60)




# =============================================================================


# =============================================================================
# Begin GUI session
# =============================================================================
root.mainloop()
