# inflation_predictor

A Python app that tracks, analyzes, and predicts future price trends of ordinary consumer products using machine learning.

- The user enters the prices of his or her favorite items at the store after every shopping trip into a user-friendly GUI.
- The program keeps track of the item, the store, the date, and the price.
- On command, the program scrapes a set of economic data points from the web and bundles it all into a machine learning training set.
- The program performs a linear regression algorithm and displays a future price trend on an individual item basis. Key timeframes are highlighted, e.g. "The 5lb bag of Red delicious apples from the Wake forest Walmart is predicted to cost $6.44 a month from now."

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
<p>Now, enter the prices you gathered from your shopping trip. Click in the entry field next to the dollar sign, enter the price, and then press Enter. The cursor will jump to the next entry field automatically for fast data entry.</p>
<p>If you make a mistake, simply click the Edit button next to that item.</p>
<p>**Note:** To skip adding a price for a certain item, simply leave the entry field blank. Do not enter "0".</p>
<p>Once all of the data has been entered, click the Save button. This will write all of the items and their price data to text files to be automatically loaded the next time you open the app. You can also view these text files as simple tabular lists of individual item's prices at certain dates.</p>

<p align="center">
  <img src="https://github.com/jmsbutcher/inflation_predictor/blob/master/Images/GUI-entry_2.png">
</p>

<p>Now you are done! You may close the app and go on putting your groceries away. Next time you go shopping, open the app and enter the prices again for that date. Over months and years, you will have accumulated a wealth of price data for the items you usually buy.</p>

### Step 5: Plot Price Trends
<p>After you have entered some data over a span of time, you can begin checking on price trends.</p>
<p>Go over to the frame on the right, titled: "Make Price Predictions."</p>
<p>Select an item from the drop down menu and click "Plot".</p>
<p>A chart will be plotted showing all the prices you entered at their corresponding dates.</p>

<p align="center">
  <img src="https://github.com/jmsbutcher/inflation_predictor/blob/master/Images/GUI-plot_1.png">
</p>

<p>To get a very basic idea of the price trend, click the checkbox labelled "Show Trendline." The program will use Numpy's polyfit regression model to plot a dotted line approximating the trend. Increase or decrease the polynomial order to get a curve that represents the data best.</p>

### Step 6: Predict Future Prices
<p>[ Under Development ]</p>
<p>The program also has a feature to predict the prices of items a set timeframe into the future.</p>
<p>Select the timeframe from the drop down menu and click "Predict".</p>
<p>The program will then use price data changes over that timeframe, as well as economic data such as CPI, Money supply, etc. at the dates at which you entered price data, to predict what the price will be in the future.</p>
<p>It first scrapes economic data from the St. Louis Federal Reserve webpage for only those dates listed in your price data, which results in very fast ( < 1 sec ) data retrieval. It packages this data into a Pandas data frame for processing.</p>
<p>It then uses regularized linear regression (scikit-learn's Ridge linear model) to fit a prediction curve to all the data. </p>
<p>Then it plots the curve on the chart. The prediction curve appears as a red dashed line.</p>
<p>The exact predicted price is indicated at the end of the last point, extended *timeframe* into the future from today.</p>
<p>You can adjust the regularization coefficient to address overfitting. Try increasing the coefficient from 0.001 by multiples of 10 (0.001, 0.01, 0.1, 1.0, etc.) and then click "Predict" again to see if the prediction curve makes more sense.</p>

<p align="center">
  <img src="https://github.com/jmsbutcher/inflation_predictor/blob/master/Images/GUI-plot_2.png">
</p>

<p>You can choose the toggle the simple linear regression trendline alongside the more complicated one to compare. Sometimes the naive approach works best, although with enough data, and enough large economic events (inflation, CPI changes, money supply changes, etc.) the intelligent model may learn to make better predictions anticipating price changes on items.</p>

<p>[ Future work: increase number of economic data points; utilize RNNs, which are perfectly suited to temporal data prediction tasks such as this. ]</p>

<p>
© 2020 James Butcher
<br>
jmsbutcher1576@gmail.com
</p>
