# Author: James Mejia
# Date: 9/21/2020
# Description: Code from https://www.geeksforgeeks.org/how-to-create-a-candlestick-chart-in-matplotlib/


import pandas as pd
import matplotlib.pyplot as plt


def candlesticks(df: pd.DataFrame):
	# Shows a candlestick chart from the parameter 'df' DataFrame

	plt.figure()

	# "up" dataframe will store the stock_prices
	# when the closing stock price is greater
	# than or equal to the opening stock prices
	up = df[df.close >= df.open]

	# "down" dataframe will store the stock_prices
	# when the closing stock price is
	# less than the opening stock prices
	down = df[df.close < df.open]

	# When the stock prices have decreased, then it
	# will be represented by blue color candlestick
	col1 = 'red'

	# When the stock prices have increased, then it
	# will be represented by green color candlestick
	col2 = 'green'

	# Setting width of candlestick elements
	width = .3
	width2 = .03

	# Plotting up prices of the stock
	plt.bar(up.index, up.close - up.open, width, bottom=up.open, color=col2)
	plt.bar(up.index, up.high - up.close, width2, bottom=up.close, color=col2)
	plt.bar(up.index, up.low - up.open, width2, bottom=up.open, color=col2)

	# Plotting down prices of the stock
	plt.bar(down.index, down.close - down.open, width, bottom=down.open, color=col1)
	plt.bar(down.index, down.high - down.open, width2, bottom=down.open, color=col1)
	plt.bar(down.index, down.low - down.close, width2, bottom=down.close, color=col1)

	# rotating the x-axis tick labels at 30degree
	# towards right
	plt.xticks(rotation=30, ha='right')

	# displaying candlestick chart of stock data
	# of a week
	plt.show()

