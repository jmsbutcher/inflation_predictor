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

Then click the "Enter" button.

### Step 3: Enter New Items to Track
If you are adding new items
