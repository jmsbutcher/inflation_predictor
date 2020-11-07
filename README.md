# inflation_predictor

A Python app that tracks, analyzes, and predicts future price trends of ordinary consumer products using machine learning.

- The user enters the prices of his or her favorite items at the store after every shopping trip into a user-friendly GUI.
- The program keeps track of the item, the store, the date, and the price.
- On command, the program scrapes a set of economic data points from the web and bundles it all into a machine learning training set.
- The program performs a linear regression algorithm and displays a future price trend on an individual item basis. Key timeframes are highlighted, e.g. "The 5lb bag of Red delicious apples from the Wake forest Walmart is predicted to cost $6.44 a month from now."
<br>
<p align="center">
  <img src="https://github.com/jmsbutcher/inflation_predictor/blob/master/Images/GUI_4.png">
</p>

## Keeping track of item prices

At its most basic level, the app acts as a simple price tracker.

### Step 1: Select Date
The first step is to select the date. The date displayed in the entry box is *today's* date by default. If you are entering shopping data from a previous date, simply type that date in standard format *YYYY-MM-DD*.

### Step 2: Select Store
The first time you visit a store, type in the store name and location. Previously entered stores will appear as a drop down menu.

<p align="center">
  <img src="https://github.com/jmsbutcher/inflation_predictor/blob/master/Images/GUI-store_entry.png">
</p>

Then click the "Enter" button. At this point, any previously tracked items will appear in a list to the right.

### Step 3: Enter New Items to Track
If you are adding new items, type in the item type, description, and quantity, and then click "Enter" for each new item. The items will be added to the list on the right.

<p align="center">
  <img src="https://github.com/jmsbutcher/inflation_predictor/blob/master/Images/GUI-entry_1.png">
</p>

### Step 4: Enter Prices
Now, enter the prices you gathered from your shopping trip. Click in the entry field next to the dollar sign, enter the price, and then press Enter. The cursor will jump to the next entry field automatically for fast data entry. If you make a mistake, simply click the Edit button next to that item. 
**Note:** To skip adding a price for a certain item, simply leave the entry field blank. Do not enter "0".
Once all of the data has been entered, click the Save button. This will write all of the items and their price data to text files to be automatically loaded the next time you open the app.

<p align="center">
  <img src="https://github.com/jmsbutcher/inflation_predictor/blob/master/Images/GUI-entry_2.png">
</p>


