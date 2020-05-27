#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:22:44 2020

@author: JamesButcher
"""

from datetime import date
from pathlib import Path
from tkinter.ttk import  Combobox
from tkinter import Button, Checkbutton, END, Entry, Frame, IntVar, \
                    Label, StringVar, Tk
from item import Item
import data_analysis

# Dictionary of Item objects --- { [Item.item_description] : [Item], ...  }
item_list = {}


# =============================================================================
# General functions
# =============================================================================
def apply_new_item(*args):
    """ Create a new item using the info entered in the new item frame and
        add it to the item list.
    """
    # Get values from entry boxes
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

    # Clear text from data entry fields
    item_type_entry.delete(0, END)
    item_desc_entry.delete(0, END)
    item_unit_entry.delete(0, END)
    
    # Move text entry focus back to top for fast data entry
    item_type_entry.focus_set()
    
def apply_store_selection(*args):
    """ Search the item list for all items that match the store name
        and location selected and generate Item_entrys for each.
    """
    # Remove blue "Saved" message, indicating a new saveable change
    saved_label.grid_remove()
    # Reset the item entry frame
    del item_entries[:]
    existing = exis_item_frame.winfo_children()
    for frame in existing:
        frame.destroy()
    # Add title message    
    existing_items_label = Label(exis_item_frame, font=("Arial", 16),
                           text="Items you've tracked before from this store:")
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
    more_items_to_add = True
    while more_items_to_add:
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
                
def save(*args):
    """ Save all item data to item folder """
    print("Saving...")
    folder = Path.cwd() / "items"
    # Create a file for each item, titled "[description].txt"
    for description, item in item_list.items():
        filename = folder / (description.lower().replace(" ", "_") + ".txt")
        with open(filename, "w") as f:
            f.write(item.to_string())
    print("Save complete")
    # Display blue "Saved" message in bottom right corner of GUI
    saved_label.grid(row=3, column=2)

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
    

class Item_entry:
    
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
        self.description_label = Label(self.item_frame, text=self.label_text)
        self.description_label.grid(row=0, column=0)
        # Create and place contents of frame
        if not item.price_entered_already_today():
            self.generate_price_entry_box()
        else:
            self.generate_price_label_box()
            
    def apply_price_entry(self, *args):
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
        
    def destroy(self):
        self.item_frame.destroy()
        
    def edit(self, *args):
        """ Remove today's price entry from item object and allow you to enter
            a new price 
        """
        self.item.remove_todays_price_entry()
        self.price_label.destroy()
        self.edit_button.destroy()
        self.generate_price_entry_box()
        self.price_entry_box.focus_set()
        
    def generate_price_entry_box(self):
        """ Create and place a price entry box """
        self.price_var = StringVar()
        self.price_entry_box = Entry(self.item_frame, 
                                     textvariable=self.price_var, 
                                     width=5)
        self.price_entry_box.grid(row=0, column=1)
        self.price_entry_box.bind("<Return>", self.apply_price_entry)
      
    def generate_price_label_box(self):
        """ - Create and place a text label of the new price
            - Create and place an Edit button to change back to a price
                entry box
        """
        price_text = "{:.2f}".format(self.item.price_data[-1][1])
        self.price_label = Label(self.item_frame, text=price_text)
        self.price_label.grid(row=0, column=1)
        
        self.edit_button = Button(self.item_frame, text="Edit", 
                              command=self.edit)
        self.edit_button.grid(row=0, column=2)
        self.edit_button.bind("<Return>", self.edit)
        
        
# =============================================================================
# Run main program
# =============================================================================

load()

# Print all existing item info 
print("\n Item list: \n", item_list, "\n")
for item in item_list.values():
    item.print_info()
    print("\n")
    

# =============================================================================
# Set up GUI
# =============================================================================
root = Tk()
root.title("Inflation Predictor")

# List of Item objects that match selected store
store_matched_items = []

# List of Item_entry objects currently in the price entry frame
item_entries = []

# Entry field variables
date_var = StringVar()
store_var = StringVar()
location_var = StringVar()
item_type_var = StringVar()
item_desc_var = StringVar()
item_unit_var = StringVar()
item_sb_var = IntVar()


# =============================================================================
# Entry frame: Main frame for entering new product and price info
# =============================================================================
entry_frame = Frame(root)
entry_frame.pack(expand=1)
entry_frame_title = Label(entry_frame, text="Enter data from shopping trip:")
entry_frame_title.grid(row=0, columnspan=2)


# =============================================================================
# Sub-frame of entry frame:
#   Date and store selector
# =============================================================================
store_frame = Frame(entry_frame, borderwidth=4, relief="ridge")
store_frame.grid(row=1, column=0, pady=30)

date_label = Label(store_frame, text="Date:")
date_label.grid(row=0, column=0, sticky="W", padx=10, pady=10)
date_entry_box = Entry(store_frame, textvariable=date_var)
date_entry_box.insert(1, str(date.today()))
date_entry_box.grid(row=0, column=1)

store_label = Label(store_frame, text="Store name:")
store_label.grid(row=1, column=0, sticky="W")

def load_store_locations(*args):
    """ Create a set of store locations that contains all the store locations
        saved in the item list for the store name currently selected in the 
        store selection combobox, and list those store locations in the 
        store location combobox
    """
    store_locations = {l.store_location for l in item_list.values() if \
                       l.store_name == store_var.get()}
    store_location_entry_box["values"] = tuple(store_locations)
    store_location_entry_box.current(0)

# Select from a list of all the different stores found in the item list
store_entry_box = Combobox(store_frame, textvariable=store_var)
store_entry_box.grid(row=1, column=1)
stores = {s.store_name for s in item_list.values()}
store_entry_box["values"] = tuple(stores)
store_entry_box.current(0)
store_entry_box.bind("<<ComboboxSelected>>", load_store_locations)

store_location_label = Label(store_frame, text="Location:")
store_location_label.grid(row=2, column=0, sticky="W")
store_location_entry_box = Combobox(store_frame, width=40, 
                                 textvariable=location_var)
store_location_entry_box.grid(row=3, columnspan=2, padx=10, pady=10)
store_location_entry_box.bind("<Return>", apply_store_selection)

load_store_locations()

store_enter_button = Button(store_frame, 
                            text="Enter", 
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
    
def toggle_sb_checkbox(*args):
    item_sb_checkbox.toggle()

item_sb_label = Label(new_frame, text="Is the item a store brand?:")
item_sb_label.grid(row=4, column=0, sticky="W")
item_sb_checkbox = Checkbutton(new_frame, variable=item_sb_var)
item_sb_checkbox.var = item_sb_var
item_sb_checkbox.grid(row=4, column=1, sticky="W")
item_sb_checkbox.bind("<Return>", toggle_sb_checkbox)

item_enter_button = Button(new_frame, text="Enter", command=apply_new_item)                  
item_enter_button.grid(row=5)
item_enter_button.bind("<Return>", apply_new_item)


# =============================================================================
# Sub-frame of entry frame:
#   List of existing items tracked at selected store
#   Used for price entry
# =============================================================================
exis_item_frame = Frame(entry_frame, borderwidth=4, relief="ridge")
exis_item_frame.grid(row=1, rowspan=2, column=1, padx=5, pady=5)

# Save button that writes all item and their corresponding price data 
#   to files in the items folder
save_button = Button(entry_frame, text="Save", command=save)
save_button.grid(row=3, column=1, sticky="SE", padx=5, pady=5)
save_button.bind("<Return>", save)

# A blue "Saved" message that appears only after pressing the save button
saved_label = Label(entry_frame, text="Saved", foreground="blue")

#print(data_analysis.convert_price_data_to_training_set(list(item_list.values())[1]))

data_analysis.convert_price_data_to_training_set(list(item_list.values())[2])

# =============================================================================
# Begin GUI session
# =============================================================================
root.mainloop()
